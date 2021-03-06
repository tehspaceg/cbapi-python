#!/usr/bin/env python

from ..oldmodels import BaseModel, immutable, MutableModel
from ..models import MutableBaseModel, CreatableModelMixin, NewBaseModel
from contextlib import closing

from zipfile import ZipFile
import six
if six.PY3:
    from io import BytesIO as StringIO
else:
    from cStringIO import StringIO


class EnforcementLevel:
    LevelHigh = 20
    LevelMedium = 30
    LevelLow = 40
    LevelNone = 80


class ApprovalRequest(MutableModel):
    urlobject = "/api/bit9platform/v1/approvalRequest"

    ResolutionNotResolved = 0
    ResolutionRejected = 1
    ResolutionApproved = 2
    ResolutionRuleChange = 3
    ResolutionInstaller = 4
    ResolutionUpdater = 5
    ResolutionPublisher = 6
    ResolutionOther = 7

    StatusSubmitted = 1
    StatusOpen = 2
    StatusClosed = 3

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(ApprovalRequest, self).__init__(cb, model_unique_id, initial_data)

    @property
    def fileCatalog(self):
        return self._join(FileCatalog, "fileCatalogId")

    @property
    def installerFileCatalog(self):
        return self._join(FileCatalog, "installerFileCatalogId")

    @property
    def processFileCatalog(self):
        return self._join(FileCatalog, "processFileCatalogId")

    @property
    def computer(self):
        return self._join(Computer, "computerId")


class Certificate(MutableModel):
    urlobject = "/api/bit9platform/v1/certificate"

    StateUnapproved = 1
    StateApproved = 2
    StateBanned = 3
    StateMixed = 4

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(Certificate, self).__init__(cb, model_unique_id, initial_data)

    @property
    def parent(self):
        return self._join(Certificate, "parentCertificateId")

    @property
    def publisher(self):
        return self._join(Publisher, "publisherId")

    @property
    def firstSeenComputer(self):
        return self._join(Computer, "firstSeenComputerId")


class Computer(MutableBaseModel):
    urlobject = "/api/bit9platform/v1/computer"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(Computer, self).__init__(cb, model_unique_id, initial_data)

    @property
    def policy(self):
        return self._join(Policy, "policyId")

    @policy.setter
    def policy(self, new_policy_id):
        self.policyId = new_policy_id

    @property
    def fileInstances(self):
        return self._cb.select(FileInstance).where("computerId:{0:d}".format(self.id))

    @property
    def template(self):
        return self._join(Computer, "templateComputerId")


class Connector(MutableBaseModel, CreatableModelMixin):
    urlobject = "/api/bit9platform/v1/connector"
    swagger_meta_file = "protection/models/connector.yaml"

    @property
    def pendingAnalyses(self):
        return self._cb.select(PendingAnalysis).where("connectorId:{0:d}".format(self.id))


@immutable
class Event(BaseModel):
    urlobject = "/api/bit9platform/v1/event"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(Event, self).__init__(cb, model_unique_id, initial_data)


class FileAnalysis(MutableModel):
    urlobject = "/api/bit9platform/v1/fileAnalysis"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(FileAnalysis, self).__init__(cb, model_unique_id, initial_data)


@immutable
class FileCatalog(BaseModel):
    urlobject = "/api/bit9platform/v1/fileCatalog"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(FileCatalog, self).__init__(cb, model_unique_id, initial_data)

    @property
    def computer(self):
        return self._cb.select(Computer, self.computerId)

    @property
    def publisher(self):
        return self._cb.select(Publisher, self.publisherId)

    @property
    def certificate(self):
        return self._cb.select(Certificate, self.certificateId)

    @property
    def fileHash(self):
        return getattr(self, "md5", None) or getattr(self, "sha1", None) or getattr(self, "sha256", None)


class FileInstance(MutableModel):
    urlobject = "/api/bit9platform/v1/fileInstance"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(FileInstance, self).__init__(cb, model_unique_id, initial_data)

    @property
    def computer(self):
        return self._cb.select(Computer, self.computerId)

    @property
    def fileCatalog(self):
        return self._cb.select(FileCatalog, self.fileCatalogId)


@immutable
class FileInstanceDeleted(BaseModel):
    urlobject = "/api/bit9platform/v1/fileInstanceDeleted"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(FileInstanceDeleted, self).__init__(cb, model_unique_id, initial_data)


@immutable
class FileInstanceGroup(BaseModel):
    urlobject = "/api/bit9platform/v1/fileInstanceGroup"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(FileInstanceGroup, self).__init__(cb, model_unique_id, initial_data)


class FileRule(MutableModel):
    urlobject = "/api/bit9platform/v1/fileRule"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(FileRule, self).__init__(cb, model_unique_id, initial_data)


class FileUpload(MutableModel):
    urlobject = "/api/bit9platform/v1/fileUpload"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(FileUpload, self).__init__(cb, model_unique_id, initial_data)

    @property
    def file(self):
        with closing(self._cb.session.get(self._build_api_request_uri() + "?downloadFile=true", stream=True)) as r:
            z = StringIO(r.content)
            zf = ZipFile(z)
            fp = zf.open(zf.filelist[0], "r")
            return fp


@immutable
class InternalEvent(BaseModel):
    urlobject = "/api/bit9platform/v1/fileInstance"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(InternalEvent, self).__init__(cb, model_unique_id, initial_data)


@immutable
class MeteredExecution(BaseModel):
    urlobject = "/api/bit9platform/v1/meteredExecution"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(MeteredExecution, self).__init__(cb, model_unique_id, initial_data)


class Notification(MutableBaseModel, CreatableModelMixin):
    ResultNotAvailable = 0
    ResultClean = 1
    ResultPotentialThreat = 2
    ResultMalicious = 3

    urlobject = "/api/bit9platform/v1/notification"
    swagger_meta_file = "protection/models/notification.yaml"


@immutable
class Notifier(BaseModel):
    urlobject = "/api/bit9platform/v1/notifier"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(Notifier, self).__init__(cb, model_unique_id, initial_data)


class PendingAnalysis(MutableModel):
    urlobject = "/api/bit9platform/v1/pendingAnalysis"

    StatusScheduled = 0
    StatusSubmitted = 1
    StatusProcessed = 2
    StatusAnalyzed = 3
    StatusError = 4
    StatusCancelled = 5

    ResultNotAvailable = 0
    ResultClean = 1
    ResultPotentialThreat = 2
    ResultMalicious = 3

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(PendingAnalysis, self).__init__(cb, model_unique_id, initial_data)

    @property
    def file(self):
        with closing(self._cb.session.get(self._build_api_request_uri() + "?downloadFile=true", stream=True)) as r:
            z = StringIO(r.content)
            zf = ZipFile(z)
            fp = zf.open(zf.filelist[0], "r")
            return fp

    def create_notification(self, **kwargs):
        n = self._cb.create(Notification, **kwargs)
        n.fileAnalysisId = self.id
        return n

    @property
    def fileCatalog(self):
        return self._cb.select(FileCatalog, self.fileCatalogId)

    @property
    def fileHash(self):
        return getattr(self, "md5", None) or getattr(self, "sha1", None) or getattr(self, "sha256", None)


class Policy(NewBaseModel):
    urlobject = "/api/bit9platform/v1/policy"


class Publisher(MutableModel):
    urlobject = "/api/bit9platform/v1/publisher"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(Publisher, self).__init__(cb, model_unique_id, initial_data)


@immutable
class ServerConfig(BaseModel):
    urlobject = "/api/bit9platform/v1/serverConfig"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(ServerConfig, self).__init__(cb, model_unique_id, initial_data)


@immutable
class ServerPerformance(BaseModel):
    urlobject = "/api/bit9platform/v1/serverPerformance"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(ServerPerformance, self).__init__(cb, model_unique_id, initial_data)


class Updater(MutableModel):
    urlobject = "/api/bit9platform/v1/updater"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(Updater, self).__init__(cb, model_unique_id, initial_data)


