from .querybuilder import QueryBuilder
from .configvalidator import ConfigValidator
from ..exceptions import EntriesException, ConfigException
from .entriesloader import EntriesLoader
from .conflict import ManualConflictResolver, AutomaticConflictResolver

class SyncArgumentsFetcher():
    def __init__(self, config, getNotes, dialog):
        self.configValidator = ConfigValidator(config)
        self.entriesLoader = EntriesLoader()
        self.queryBuilder = QueryBuilder()
        self.manualConflictResolver = ManualConflictResolver(dialog)
        self.automaticConflictResolver = AutomaticConflictResolver()
        self.getNotes = getNotes

    def fetch(self, extendedQuery, skipTagged, resolveManually):
        config = self.configValidator.validate()
        entries = self.entriesLoader.getEntries(config.entriesFile)
        conflictResolver = self.manualConflictResolver if resolveManually else self.automaticConflictResolver
        query = self.queryBuilder.build(config.noteType, skipTagged, extendedQuery)
        notes = self.getNotes(query)

        return SyncArguments(notes, entries, conflictResolver, config.audioDirectory)

class SyncArguments():
    def __init__(self, notes, entries, conflictResolver, audioDirectory):
        self.notes = notes
        self.entries = entries
        self.conflictResolver = conflictResolver
        self.audioDirectory = audioDirectory