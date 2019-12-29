import re
from datetime import timedelta

re_lang_time_room = re.compile(
    r"^\[(?P<language>[a-z-_]{2,5})\] (?P<time>\d\d:\d\d) \+(?P<duration>\d\d:\d\d), (?P<room>.*)$"
)
re_fahrplan = re.compile(r"^Fahrplan: (?P<url>http.*)$")
re_translators = re.compile(
    r"^→\s*(?P<language>[a-z-_]{2,5})\s*:?\s*(\[(?P<partial>.*-.*)\])?\s*(?P<translators>.*)$"
)

# Parenthetical stuff in shift assignments that should be removed
re_parentheses = re.compile(r"\s*\(.*?\)\s*|\s[-–].*")


class Error(Exception):
    pass


class ParseError(Error):
    def __init__(self, line):
        self.message = "Error parsing the following line:\n\t%s" % line


def parse_time(timestring):
    [hours, minutes] = timestring.split(':')
    return timedelta(hours=int(hours), minutes=int(minutes))


class TranslationShift:
    def __init__(self, name, language, talk=None, partial=None):
        self.name = name
        self.language = language
        self.talk = talk
        self.partial = partial

        self.duration = talk.duration
        if self.partial:
            [start, end] = self.partial.split('-')
            self.duration = parse_time(end) - parse_time(start)

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.language == other.language
            and self.talk == other.talk
        )

    def __repr__(self):
        return 'TranslationShift(name="%s", language="%s", Talk=%s)' % (
            self.name,
            self.language,
            self.talk.__repr__(),
        )

    def to_json(self):
        return {
            "name": self.name,
            "language": self.language,
            "talk": (self.talk.__dict__ if self.talk else None),
        }


class Talk:
    def __init__(self, block):
        """
        Parse a block of translation assignments from the talks pad.

        Blocks span mutliple lines and follow this pattern:
            #1
            [de] 11:00 +00:30, Adams
            Opening Event
            rufus, rixx
            Fahrplan: https://fahrplan.events.ccc.de/congress/2018/Fahrplan/events/9985.html
            Slides (if available): https://speakers.c3lingo.org/talks/15f4e5c5-40e1-4c73-8da0-4cc2a773ab13/
            → en: waffle, simplysaym, sirenensang
            → fr: informancer, ironic, yann0u

        Blocks that don't start with a # sign will return None, blocks that *do* start with # will
        return a dict representing this talk or raise an exception.
        """
        state = None
        self.translation_shifts = []

        for line in block.splitlines():
            if state == "title":
                self.title = line
                state = "speakers"
                continue

            if state == "speakers":
                self.speakers = line.split(", ")
                state = None
                continue

            match = re_lang_time_room.match(line)
            if match:
                self.language = match.group("language")
                self.room = match.group("room")
                duration = match.group("duration").split(":")
                self.duration = timedelta(
                    hours=int(duration[0]), minutes=int(duration[1])
                )
                state = "title"
                continue

            match = re_fahrplan.match(line)
            if match:
                self.fahrplan = match.group("url")
                continue

            match = re_translators.match(line)
            if match:
                language = match.group("language")
                partial = match.group("partial")
                # strip out parentheses first
                translators = re_parentheses.sub("", match.group("translators")).strip()
                for name in translators.split(","):
                    name = name.strip()
                    if name == "":
                        continue
                    self.translation_shifts.append(
                        TranslationShift(name=name, language=language, talk=self, partial=partial)
                    )
                continue

            # If the contains nothing but an arrow, ignore it
            if line.strip() == "→":
                continue

            # If the row starts with an arrow but didn't match yet, there's probably a syntax error
            if line[0] == "→":
                raise ParseError(line)


def parse_block(block):
    block = block.strip()
    if block[0] != "#":
        return None
    return Talk(block)


def parse_file(file):
    return [
        block
        for block in map(parse_block, re.split(u"\n{2,}", file.strip()))
        if block != None
    ]
