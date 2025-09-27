from __future__ import annotations
from typing import Any, Optional, Literal, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import urllib.parse
import json
import base64
import requests


class AccountKind(str, Enum):
    STUDENT = "E"


class GradeKind(int, Enum):
    ERROR = -1
    GRADE = 0
    ABSENT = 1
    EXEMPTED = 2
    NOT_GRADED = 3
    WAITING = 4


class FileKind(str, Enum):
    CLOUD = "CLOUD"
    HOMEWORK = "FICHIER_CDT"
    ATTACHMENT = "PIECE_JOINTE"
    CANTINE_MENU = "FICHIER_MENU_RESTAURATION"
    ADMINISTRATIVE = "ADMINISTRATIF"
    OTHER = ""


class DocumentKind(str, Enum):
    GRADES = "Note"
    DOCUMENT = "Doc"
    SCHOOL_LIFE = "Viesco"
    INVOICE = "Fac"
    REGISTRATION = "Inscr"
    TEXTBOOK = "FICHIER_CDT"
    OTHER = ""


class AttendanceItemKind(str, Enum):
    PUNITION = "Punition"
    RETARD = "Retard"
    ABSENCE = "Absence"
    DISPENSE = "Dispense"


class TimetableItemKind(str, Enum):
    COURS = "COURS"
    PERMANENCE = "PERMANENCE"
    CONGE = "CONGE"
    EVENEMENT = "EVENEMENT"
    SANCTION = "SANCTION"


class TimelineItemKind(str, Enum):
    NOTE = "Note"
    VIE_SCOLAIRE = "VieScolaire"
    REUNION_PP = "ReunionPP"
    REUNION_PP_FAMILLE = "ReunionPPFamille"
    ACTUALITE = "Actualite"
    MESSAGERIE = "Messagerie"
    DOCUMENT_FAMILLE = "DocumentFamille"
    DOCUMENT = "Document"


class WorkspaceItemKind(str, Enum):
    LIBRE = "LIBRE"


class BadCredentials(Exception):
    pass


class DoubleAuthRequired(Exception):
    pass


class InvalidVersion(Exception):
    pass


class SessionTokenRequired(Exception):
    pass


class BadDoubleAuth(Exception):
    pass


@dataclass
class DoubleAuth:
    name: str
    value: str


@dataclass
class DoubleAuthChallenge:
    question: str
    answers: list[str]


@dataclass
class Session:
    username: str
    device_uuid: str
    token: Optional[str] = None
    access_token: Optional[str] = None
    double_auth: Optional[DoubleAuth] = None
    fetcher: Optional[Callable] = None


@dataclass
class Account:
    login_id: int
    id: int
    user_id: str
    username: str
    kind: AccountKind
    ogec_id: str
    main: bool
    last_connection: str
    first_name: str
    last_name: str
    email: str
    phone: str
    school_name: str
    school_uai: str
    school_logo_path: str
    school_agenda_color: str
    access_token: str
    socket_token: str
    gender: Literal["M", "F"]
    profile_picture_url: str
    modules: list[Any]
    current_school_cycle: str
    class_short: str
    class_long: str


@dataclass
class GradeValue:
    kind: GradeKind
    points: float


@dataclass
class Skill:
    id: int
    value: float
    description: str
    name: str


@dataclass
class Subject:
    id: str
    sub_subject_id: Optional[str]
    name: str


@dataclass
class Grade:
    comment: str
    exam_type: str
    period_id: str
    period_name: str
    subject: Subject
    coefficient: float
    value: GradeValue
    max_value: GradeValue
    min_value: GradeValue
    average: GradeValue
    is_optional: bool
    out_of: float
    date: datetime
    subject_file_path: str
    correction_file_path: str
    skills: list[Skill]


@dataclass
class Period:
    id: str
    name: str
    yearly: bool
    is_mock_exam: bool
    is_ended: bool
    start_date: datetime
    end_date: datetime
    council_date: Optional[datetime] = None
    council_start_hour: Optional[str] = None
    council_end_hour: Optional[str] = None
    council_classroom: Optional[str] = None


@dataclass
class SubjectOverview:
    name: str
    id: str
    child_subject_id: str
    is_child_subject: bool
    color: str
    coefficient: float
    class_average: GradeValue
    max_average: GradeValue
    min_average: GradeValue
    student_average: GradeValue
    out_of: GradeValue


@dataclass
class PeriodOverview:
    class_average: GradeValue
    overall_average: GradeValue
    subjects: list[SubjectOverview]


@dataclass
class Document:
    id: int
    name: str
    date: datetime
    kind: DocumentKind
    signature_required: bool
    signature: Optional[Any] = None


@dataclass
class Homework:
    id: int
    subject: str
    teacher: str
    exam: bool
    done: bool
    content: str
    created_date: datetime
    attachments: list[Document]


@dataclass
class ComingHomework:
    id: int
    subject: str
    is_exam: bool
    done: bool
    created_date: datetime


@dataclass
class ClassSubject:
    date: datetime
    id: int
    subject: str
    teacher: str
    content: str
    attachments: list[Document]


@dataclass
class AttendanceItem:
    id: int
    student_id: int
    student_name: str
    reason: str
    date: datetime
    date_of_event: datetime
    label: str
    teacher: str
    comment: str
    subject_name: str
    justified: bool
    justification_type: str
    online_justification: bool
    todo: str
    kind: AttendanceItemKind
    display_date: str


@dataclass
class CantineMeals:
    breakfast: bool
    lunch: bool
    dinner: bool


@dataclass
class CantineReservations:
    badge: int
    diet: str
    meals: dict[str, CantineMeals]


@dataclass
class CantineBarcode:
    badge_number: int


@dataclass
class TimetableItem:
    id: int
    color: str
    start_date: datetime
    end_date: datetime
    subject_name: str
    subject_short_name: str
    room: str
    teacher: str
    kind: TimetableItemKind
    cancelled: bool
    updated: bool
    notes: str


@dataclass
class TimelineItem:
    title: str
    description: str
    content: str
    element_id: int
    element_kind: TimelineItemKind
    date: datetime


@dataclass
class HomepageTimelineItem:
    id: str
    content: str
    author_name: str
    creation_date: datetime
    start_date: datetime
    end_date: datetime
    color_name: str


@dataclass
class WorkspaceItem:
    id: str
    title: str
    description: str
    summary: str
    cloud: bool
    discussion: bool
    agenda: bool
    is_public: bool
    is_open: bool
    kind: WorkspaceItemKind
    is_member: bool
    is_admin: bool
    teacher_rooms: bool
    created_by: str
    permissions: int
    nb_members: int
    color_event_agenda: str
    created_at: Optional[str] = None


@dataclass
class ReceivedMessage:
    id: int
    type: str
    date: datetime
    read: bool
    subject: str
    can_answer: bool
    content: str
    sender: str
    files: list[dict[str, Any]]


class Request:
    def __init__(self, path: str):
        self.url = f"https://api.ecoledirecte.com/v3{path}"
        self.headers = {"User-Agent": "Android EDMOBILE v7.0.1"}
        self.method = "POST"
        self.content = None
        self.params = {"v": "7.0.1"}

    def set_token(self, token: str) -> Request:
        self.headers["X-Token"] = token
        return self

    def set_form_data(self, body: dict) -> Request:
        self.content = f"data={json.dumps(body)}"
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        return self

    def send(self, fetcher: Optional[Callable] = None) -> Response:
        if fetcher:
            return fetcher(self)
        response = requests.post(
            self.url,
            params=self.params,
            headers=self.headers,
            data=self.content
        )
        return Response(response)

    def send_raw(self, fetcher: Optional[Callable] = None) -> requests.Response:
        if fetcher:
            return fetcher(self)
        return requests.post(
            self.url,
            params=self.params,
            headers=self.headers,
            data=self.content
        )


class Response:
    def __init__(self, response: requests.Response):
        self.token = response.headers.get("x-token")
        self.access_token = None
        self.message = None
        self.data = None

        content_type = response.headers.get("content-type", "")
        content = response.text

        valid_json = (content.startswith(("[", "{")) and 
                     content.endswith(("]", "}")))

        if not content_type.startswith("application/json") and not valid_json:
            self.status = int(response.headers.get("x-code", 500))
        else:
            try:
                parsed = json.loads(content)
                self.status = parsed.get("code")
                self.data = parsed.get("data")
                self.message = parsed.get("message")
                if "token" in parsed:
                    self.token = parsed["token"]
            except json.JSONDecodeError:
                self.status = 500
                self.data = None


def decode_string(value: str, escape_string: bool = True) -> str:
    try:
        decoded = base64.b64decode(value).decode("utf-8")
        return urllib.parse.unquote(decoded) if escape_string else decoded
    except Exception:
        return value


def encode_string(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("utf-8")


def safe_float(value: Any, default: float = 0.0) -> float:
    if not value:
        return default
    try:
        return float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    if not value:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_datetime(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None


def decode_account_kind(kind: Any) -> AccountKind:
    kind = str(kind)
    if kind not in [e.value for e in AccountKind]:
        raise ValueError(f"Unknown AccountKind: {kind}")
    return AccountKind(kind)


def decode_account(account: dict) -> Account:
    profile = account.get("profile", {})
    gender = profile.get("sexe")
    if not gender:
        gender = "F" if account.get("civilite") == "Mme" else "M"

    return Account(
        login_id=safe_int(account.get("idLogin")),
        id=safe_int(account.get("id")),
        user_id=str(account.get("uid", "")),
        username=str(account.get("identifiant", "")),
        kind=decode_account_kind(account.get("typeCompte", "E")),
        ogec_id=str(account.get("codeOgec", "")),
        main=bool(account.get("main", False)),
        last_connection=str(account.get("lastConnexion", "")),
        first_name=str(account.get("prenom", "")),
        last_name=str(account.get("nom", "")),
        email=str(account.get("email", "")),
        phone=str(profile.get("telPortable", "")),
        school_name=str(account.get("nomEtablissement", "")),
        school_uai=str(profile.get("rneEtablissement", "")),
        school_logo_path=str(account.get("logoEtablissement", "")),
        school_agenda_color=str(account.get("couleurAgendaEtablissement", "")),
        access_token=str(account.get("accessToken", "")),
        socket_token=str(account.get("socketToken", "")),
        gender=gender,
        profile_picture_url=str(profile.get("photo", "")),
        modules=account.get("modules", []),
        current_school_cycle=str(account.get("anneeScolaireCourante", "")),
        class_short=str(profile.get("classe", {}).get("code", "")),
        class_long=str(profile.get("classe", {}).get("libelle", ""))
    )


def decode_grade_value(value: str) -> GradeValue:
    if not value:
        return GradeValue(kind=GradeKind.ERROR, points=0)

    value = value.strip()
    grade_map = {
        "Disp": GradeKind.EXEMPTED,
        "Abs": GradeKind.ABSENT,
        "NE": GradeKind.NOT_GRADED,
        "EA": GradeKind.WAITING
    }
    
    if value in grade_map:
        return GradeValue(kind=grade_map[value], points=0)
    
    return GradeValue(kind=GradeKind.GRADE, points=safe_float(value))


def decode_skill(item: dict) -> Skill:
    return Skill(
        id=safe_int(item.get("idCompetence")),
        value=safe_float(item.get("valeur")),
        description=str(item.get("descriptif", "")),
        name=str(item.get("libelleCompetence", ""))
    )


def decode_grade(item: dict) -> Grade:
    return Grade(
        comment=str(item.get("devoir", "")),
        exam_type=str(item.get("typeDevoir", "")),
        period_id=str(item.get("codePeriode", "")),
        period_name="",
        subject=Subject(
            id=str(item.get("codeMatiere", "")),
            sub_subject_id=item.get("codeSousMatiere"),
            name=str(item.get("libelleMatiere", ""))
        ),
        coefficient=safe_float(item.get("coef", 1)),
        value=decode_grade_value(str(item.get("valeur", ""))),
        max_value=decode_grade_value(str(item.get("maxClasse", ""))),
        min_value=decode_grade_value(str(item.get("minClasse", ""))),
        average=decode_grade_value(str(item.get("moyenneClasse", ""))),
        is_optional=bool(item.get("valeurisee", False)),
        out_of=safe_float(item.get("noteSur", "20")),
        date=safe_datetime(str(item.get("date", ""))) or datetime.now(),
        subject_file_path=str(item.get("uncSujet", "")),
        correction_file_path=str(item.get("uncCorrige", "")),
        skills=[decode_skill(s) for s in item.get("elementsProgramme", [])]
    )


def decode_period(item: dict) -> Period:
    start_date = safe_datetime(str(item.get("dateDebut", "")))
    end_date = safe_datetime(str(item.get("dateFin", "")))
    council_date = safe_datetime(str(item.get("dateConseil", ""))) if item.get("dateConseil") else None
    
    return Period(
        id=str(item.get("idPeriode", "")),
        name=str(item.get("periode", "")),
        yearly=bool(item.get("annuel", False)),
        is_mock_exam=bool(item.get("examenBlanc", False)),
        is_ended=bool(item.get("cloture", False)),
        start_date=start_date or datetime.now(),
        end_date=end_date or datetime.now(),
        council_date=council_date,
        council_start_hour=item.get("heureConseil"),
        council_end_hour=item.get("heureFinConseil"),
        council_classroom=item.get("salleConseil")
    )


def build_overview(data: dict) -> dict[str, PeriodOverview]:
    overview = {}
    out_of = safe_float(data.get("parametrage", {}).get("moyenneSur", 20))
    show_student_average = data.get("parametrage", {}).get("moyenneGenerale", True)
    show_yearly_period = data.get("parametrage", {}).get("notePeriodeAnnuelle", True)

    for period in data.get("periodes", []):
        if not show_yearly_period and period.get("yearly"):
            continue

        subjects = period.get("ensembleMatieres", {}).get("disciplines", [])
        class_avg = decode_grade_value(str(period.get("ensembleMatieres", {}).get("moyenneClasse", "")))
        
        if show_student_average:
            overall_avg = decode_grade_value(str(period.get("ensembleMatieres", {}).get("moyenneGenerale", "")))
        else:
            count = 0
            total = 0
            for subject in subjects:
                if subject.get("moyenne", ""):
                    grade = decode_grade_value(str(subject["moyenne"]).replace(",", ".")).points
                    coef = safe_float(subject.get("coef", 1))
                    if coef == 0:
                        coef = 1
                    count += coef
                    total += grade * coef
            overall_avg = decode_grade_value(str(total / count if count > 0 else 0))

        subject_overviews = []
        for subject in subjects:
            subject_overviews.append(SubjectOverview(
                name=str(subject.get("discipline", "")),
                id=str(subject.get("codeMatiere", "")),
                child_subject_id=str(subject.get("codeSousMatiere", "")),
                is_child_subject=bool(subject.get("sousMatiere", False)),
                color="",
                coefficient=safe_float(subject.get("coef", 1)),
                class_average=decode_grade_value(str(subject.get("moyenneClasse", "")).replace(",", ".")),
                max_average=decode_grade_value(str(subject.get("moyenneMax", "")).replace(",", ".")),
                min_average=decode_grade_value(str(subject.get("moyenneMin", "")).replace(",", ".")),
                student_average=decode_grade_value(str(subject.get("moyenne", "")).replace(",", ".")),
                out_of=decode_grade_value(str(out_of))
            ))

        overview[str(period.get("idPeriode", ""))] = PeriodOverview(
            class_average=class_avg,
            overall_average=overall_avg,
            subjects=subject_overviews
        )

    return overview


def decode_document(item: dict) -> Document:
    date = safe_datetime(str(item.get("date", "")))
    return Document(
        id=safe_int(item.get("id")),
        name=str(item.get("libelle", "")),
        date=date or datetime.now(),
        kind=DocumentKind(item.get("type", "")),
        signature_required=bool(item.get("signatureDemandee", False)),
        signature=item.get("signature")
    )


def decode_homework(item: dict) -> Homework:
    a_faire = item.get("aFaire", {})
    created_date = safe_datetime(str(a_faire.get("donneLe", "")))
    
    return Homework(
        id=safe_int(item.get("id")),
        subject=str(item.get("matiere", "")),
        teacher=str(item.get("nomProf", "")),
        exam=bool(item.get("interrogation", False)),
        done=bool(a_faire.get("effectue", False)),
        content=decode_string(str(a_faire.get("contenu", ""))),
        created_date=created_date or datetime.now(),
        attachments=[decode_document(d) for d in a_faire.get("documents", [])]
    )


def decode_coming_homework(item: dict) -> ComingHomework:
    created_date = safe_datetime(str(item.get("donneLe", "")))
    
    return ComingHomework(
        id=safe_int(item.get("idDevoir")),
        subject=str(item.get("matiere", "")),
        is_exam=bool(item.get("interrogation", False)),
        done=bool(item.get("effectue", False)),
        created_date=created_date or datetime.now()
    )


def decode_class_subject(item: dict, date: datetime) -> ClassSubject:
    content_data = item.get("contenuDeSeance", {})
    content = content_data.get("contenu", "")
    
    return ClassSubject(
        date=date,
        id=safe_int(item.get("id")),
        subject=str(item.get("matiere", "")),
        teacher=str(item.get("nomProf", "")),
        content=decode_string(str(content)) if content else "",
        attachments=[decode_document(d) for d in content_data.get("documents", [])]
    )


def decode_attendance_item(item: dict) -> AttendanceItem:
    display_date = str(item.get("displayDate", ""))
    if not display_date:
        display_date = str(item.get("dateDeroulement", "")).lower().replace("<br>", " ").replace("déroulement prévu ", "")
    
    date = safe_datetime(str(item.get("date", "")))
    date_of_event = safe_datetime(str(item.get("dateDeroulement", "")))
    
    return AttendanceItem(
        id=safe_int(item.get("id")),
        student_id=safe_int(item.get("idEleve")),
        student_name=str(item.get("nomEleve", "")),
        reason=str(item.get("motif", "")),
        date=date or datetime.now(),
        date_of_event=date_of_event or datetime.now(),
        label=str(item.get("libelle", "")),
        teacher=str(item.get("par", "")),
        comment=str(item.get("commentaire", "")),
        subject_name=str(item.get("matiere", "")),
        justified=bool(item.get("justifie", False)),
        justification_type=str(item.get("typeJustification", "")),
        online_justification=bool(item.get("justifieEd", False)),
        todo=str(item.get("aFaire", "")),
        kind=AttendanceItemKind(item.get("typeElement", "Absence")),
        display_date=display_date
    )


def decode_cantine_reservations(item: dict) -> CantineReservations:
    params = item.get("params", {})
    meals = {
        day: CantineMeals(
            breakfast=False,
            lunch=params.get(f"repasmidi_{i}", "0") == "1",
            dinner=params.get(f"repassoir_{i}", "0") == "1"
        )
        for i, day in enumerate(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"], 1)
    }
    
    return CantineReservations(
        badge=safe_int(item.get("badge")),
        diet=str(params.get("regime", "")),
        meals=meals
    )


def decode_cantine_barcode(item: dict) -> CantineBarcode:
    return CantineBarcode(
        badge_number=safe_int(item.get("params", {}).get("numeroBadge"))
    )


def decode_timetable_item(item: dict) -> TimetableItem:
    try:
        start_date = datetime.fromisoformat(str(item.get("start_date", "")))
    except ValueError:
        start_date = datetime.now()
    
    try:
        end_date = datetime.fromisoformat(str(item.get("end_date", "")))
    except ValueError:
        end_date = datetime.now()
    
    return TimetableItem(
        id=safe_int(item.get("id")),
        color=str(item.get("color", "")),
        start_date=start_date,
        end_date=end_date,
        subject_name=str(item.get("matiere", "")),
        subject_short_name=str(item.get("codeMatiere", "")),
        room=str(item.get("salle", "")),
        teacher=str(item.get("prof", "")),
        kind=TimetableItemKind(item.get("typeCours", "COURS")),
        cancelled=bool(item.get("isAnnule", False)),
        updated=bool(item.get("isModifie", False)),
        notes=str(item.get("text", ""))
    )


def decode_timeline_item(item: dict) -> TimelineItem:
    try:
        date = datetime.fromisoformat(str(item.get("date", "")))
    except ValueError:
        date = datetime.now()
    
    return TimelineItem(
        title=str(item.get("titre", "")),
        description=str(item.get("soustitre", "")),
        content=str(item.get("contenu", "")),
        element_id=safe_int(item.get("idElement")),
        element_kind=TimelineItemKind(item.get("typeElement", "NOTE")),
        date=date
    )


def decode_french_date(date_str: str) -> datetime:
    try:
        day, month, year = date_str.split("/")
        return datetime(int(year), int(month), int(day))
    except ValueError:
        return datetime.now()


def decode_homepage_timeline_item(item: dict) -> HomepageTimelineItem:
    return HomepageTimelineItem(
        id=str(item.get("id", "")),
        content=decode_string(str(item.get("contenu", ""))),
        author_name=str(item.get("auteur", {}).get("nom", "")),
        creation_date=decode_french_date(str(item.get("dateCreation", "01/01/2000"))),
        start_date=decode_french_date(str(item.get("dateDebut", "01/01/2000"))),
        end_date=decode_french_date(str(item.get("dateFin", "01/01/2000"))),
        color_name=str(item.get("type", ""))
    )


def decode_workspace_item(item: dict) -> WorkspaceItem:
    return WorkspaceItem(
        id=str(item.get("id", "")),
        title=str(item.get("titre", "")),
        description=str(item.get("description", "")),
        summary=decode_string(str(item.get("resume", ""))),
        cloud=bool(item.get("cloud", False)),
        discussion=bool(item.get("discussion", False)),
        agenda=bool(item.get("agenda", False)),
        is_public=bool(item.get("public", False)),
        is_open=bool(item.get("ouvert", False)),
        kind=WorkspaceItemKind(item.get("type", "LIBRE")),
        is_member=bool(item.get("estMembre", False)),
        is_admin=bool(item.get("estAdmin", False)),
        teacher_rooms=bool(item.get("salleDesProfs", False)),
        created_by=str(item.get("creePar", "")),
        permissions=safe_int(item.get("droitUtilisateur")),
        nb_members=safe_int(item.get("nbMembres")),
        color_event_agenda=str(item.get("couleurEvenementAgenda", "")),
        created_at=item.get("creeLe")
    )


def decode_message_list(message: dict) -> ReceivedMessage:
    sender_data = message.get("from", {})
    try:
        date = datetime.fromisoformat(str(message.get("date", "")))
    except ValueError:
        date = datetime.now()
    
    return ReceivedMessage(
        id=safe_int(message.get("id")),
        type=str(message.get("mtype", "")),
        date=date,
        read=bool(message.get("read", False)),
        subject=str(message.get("subject", "")),
        can_answer=bool(message.get("canAnswer", False)),
        content=str(message.get("content", "")),
        sender=f"{sender_data.get('prenom', '')} {sender_data.get('nom', '')}".strip(),
        files=[{
            "id": f.get("id"),
            "name": str(f.get("libelle", "")),
            "type": FileKind(f.get("type", ""))
        } for f in message.get("files", [])]
    )


def encode_double_auth(double_auth: Optional[DoubleAuth]) -> Optional[dict]:
    if not double_auth:
        return None
    return {"cn": double_auth.name, "cv": double_auth.value}


def decode_double_auth_challenge(challenge: dict) -> DoubleAuthChallenge:
    return DoubleAuthChallenge(
        question=decode_string(str(challenge.get("question", ""))),
        answers=[decode_string(str(a)) for a in challenge.get("propositions", [])]
    )


def decode_double_auth(double_auth: Any) -> DoubleAuth:
    if double_auth is None:
        raise BadDoubleAuth()
    return DoubleAuth(
        name=str(double_auth.get("cn", "")), 
        value=str(double_auth.get("cv", ""))
    )


def init_login(body: dict, token: Optional[str] = None) -> Request:
    request_gtk = Request("/login.awp?gtk=1")
    response_gtk = request_gtk.send_raw()
    
    cookies = []
    gtk = None
    
    for cookie in response_gtk.cookies:
        cookies.append(f"{cookie.name}={cookie.value}")
        if cookie.name == "GTK":
            gtk = cookie.value
    
    if not gtk:
        raise Exception("GTK cookie not found")
    
    request = Request("/login.awp")
    request.set_form_data(body)
    request.headers["X-GTK"] = gtk
    request.headers["Cookie"] = "; ".join(cookies)
    
    if token:
        request.set_token(token)
    
    return request


def login(session: Session, password: str) -> list[Account]:
    encoded_double_auth = encode_double_auth(session.double_auth)
    
    body = {
        "identifiant": session.username,
        "uuid": session.device_uuid,
        "isReLogin": False,
        "sesouvenirdemoi": True,
        "motdepasse": urllib.parse.quote(password)
    }
    
    if encoded_double_auth:
        body.update(encoded_double_auth)
        body["fa"] = [encoded_double_auth]
    
    request = init_login(body, session.token)
    response = request.send(session.fetcher)
    
    session.token = response.token
    
    if response.status == 505:
        raise BadCredentials()
    elif response.status == 517:
        raise InvalidVersion()
    elif response.status == 250:
        raise DoubleAuthRequired()
    
    return [decode_account(acc) for acc in response.data.get("accounts", [])]


def refresh(session: Session, account_kind: AccountKind) -> list[Account]:
    if not session.token:
        raise SessionTokenRequired()
    
    body = {
        "fa": [encode_double_auth(session.double_auth)],
        "identifiant": session.username,
        "uuid": session.device_uuid,
        "isReLogin": True,
        "motdepasse": "???",
        "typeCompte": account_kind.value,
        "accesstoken": session.access_token
    }
    
    request = init_login(body, session.token)
    response = request.send(session.fetcher)
    
    session.token = response.token
    
    if response.status == 505:
        raise BadCredentials()
    elif response.status == 517:
        raise InvalidVersion()
    elif response.status == 250:
        raise DoubleAuthRequired()
    
    return [decode_account(acc) for acc in response.data.get("accounts", [])]


def set_access_token(session: Session, account: Account):
    session.access_token = account.access_token


def init_double_auth(session: Session) -> DoubleAuthChallenge:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request("/connexion/doubleauth.awp?verbe=get")
    request.set_token(session.token).set_form_data({})
    
    response = request.send(session.fetcher)
    
    if not response.token:
        raise BadCredentials()
    
    session.token = response.token
    return decode_double_auth_challenge(response.data)


def check_double_auth(session: Session, answer: str) -> bool:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request("/connexion/doubleauth.awp?verbe=post")
    request.set_token(session.token).set_form_data({
        "choix": encode_string(answer)
    })
    
    response = request.send(session.fetcher)
    session.token = response.token
    session.double_auth = decode_double_auth(response.data)
    
    return True


def student_grades(session: Session, account: Account, year: str = "") -> dict:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request(f"/eleves/{account.id}/notes.awp?verbe=get")
    request.set_token(session.token).set_form_data({"anneeScolaire": year})
    
    response = request.send(session.fetcher)
    session.token = response.token
    
    grades = [decode_grade(g) for g in response.data.get("notes", [])]
    periods_data = response.data.get("periodes", [])
    show_yearly = response.data.get("parametrage", {}).get("notePeriodeAnnuelle", True)
    
    periods = [decode_period(p) for p in periods_data if not (not show_yearly and p.get("yearly"))]
    overview = build_overview(response.data)
    
    return {"grades": grades, "periods": periods, "overview": overview}


def student_homeworks(session: Session, account: Account, date: str) -> dict:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request(f"/Eleves/{account.id}/cahierdetexte/{date}.awp?verbe=get")
    request.set_token(session.token).set_form_data({})
    
    response = request.send(session.fetcher)
    session.token = response.token
    
    matieres = response.data.get("matieres", [])
    homeworks = [decode_homework(h) for h in matieres if h.get("aFaire")]
    
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        date_obj = datetime.now()
    
    subjects = [decode_class_subject(item, date_obj) for item in matieres]
    subjects = [s for s in subjects if s.attachments or s.content]
    
    return {"homeworks": homeworks, "subjects": subjects}


def student_coming_homeworks(session: Session, account: Account) -> list[dict]:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request(f"/Eleves/{account.id}/cahierdetexte.awp?verbe=get")
    request.set_token(session.token).set_form_data({})
    
    response = request.send(session.fetcher)
    session.token = response.token
    
    result = []
    for date_str, homeworks in response.data.items():
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            result.append({
                "date": parsed_date,
                "homeworks": [decode_coming_homework(h) for h in homeworks]
            })
        except ValueError:
            continue
    
    return result


def set_homework_state(session: Session, account: Account, homework_id: int, done: bool):
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request(f"/Eleves/{account.id}/cahierdetexte.awp?verbe=put")
    request.set_token(session.token).set_form_data({
        "idDevoirsEffectues": [homework_id if done else None],
        "idDevoirsNonEffectues": [None if done else homework_id]
    })
    
    request.send(session.fetcher)


def student_attendance(session: Session, account: Account) -> dict:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request(f"/eleves/{account.id}/viescolaire.awp?verbe=get")
    request.set_token(session.token).set_form_data({})
    
    response = request.send(session.fetcher)
    session.token = response.token
    
    return {
        "punishments": [decode_attendance_item(p) for p in response.data.get("sanctionsEncouragements", [])],
        "absences": [decode_attendance_item(a) for a in response.data.get("absencesRetards", [])],
        "exemptions": [decode_attendance_item(e) for e in response.data.get("dispenses", [])]
    }


def student_cantine(account: Account) -> dict:
    reservations_module = next((m for m in account.modules if m.get("code") == "RESERVATIONS"), None)
    barcode_module = next((m for m in account.modules if m.get("code") == "CANTINE_BARCODE"), None)
    
    result = {}
    
    if reservations_module and reservations_module.get("enable"):
        result["reservation"] = decode_cantine_reservations(reservations_module)
    
    if barcode_module and barcode_module.get("enable"):
        result["barcode"] = decode_cantine_barcode(barcode_module)
    
    return result


def student_documents(session: Session, archive: str = "") -> list[Document]:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request(f"/elevesDocuments.awp?verbe=get&archive={archive}")
    request.set_token(session.token).set_form_data({"forceDownload": 0})
    
    response = request.send(session.fetcher)
    
    all_documents = []
    for key in ["factures", "notes", "viescolaire", "administratifs", "inscriptions"]:
        all_documents.extend(response.data.get(key, []))
    
    return [decode_document(d) for d in all_documents]


def build_file_download_url(file_type: FileKind, file_id: int, year: str = "") -> str:
    endpoint = f"/telechargement.awp?verbe=get&fichierId={file_id}"
    
    if file_type == FileKind.ADMINISTRATIVE:
        return f"{endpoint}&archive=true&anneeArchive={year}" if year else endpoint
    elif file_type == FileKind.ATTACHMENT:
        return f"{endpoint}&anneeMessages={year}" if year else endpoint
    else:
        return f"{endpoint}&leTypeDeFichier={file_type.value}"


def get_file(session: Session, file_type: FileKind, file_id: int, year: str = "") -> requests.Response:
    if not session.token:
        raise SessionTokenRequired()
    
    url = build_file_download_url(file_type, file_id, year)
    request = Request(url)
    request.set_token(session.token).set_form_data({"forceDownload": 0})
    
    return request.send_raw(session.fetcher)


def student_timetable(session: Session, account: Account, start_date: datetime, end_date: Optional[datetime] = None) -> list[TimetableItem]:
    if not session.token:
        raise SessionTokenRequired()
    
    if end_date is None:
        end_date = start_date
    
    request = Request(f"/E/{account.id}/emploidutemps.awp?verbe=get")
    request.set_token(session.token).set_form_data({
        "dateDebut": start_date.strftime("%Y-%m-%d"),
        "dateFin": end_date.strftime("%Y-%m-%d"),
        "avecTrous": False
    })
    
    response = request.send(session.fetcher)
    session.token = response.token
    
    items = [decode_timetable_item(item) for item in response.data]
    items.sort(key=lambda x: x.start_date)
    
    return items


def student_timeline(session: Session, account: Account) -> list[TimelineItem]:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request(f"/eleves/{account.id}/timeline.awp?verbe=get")
    request.set_token(session.token).set_form_data({})
    
    response = request.send(session.fetcher)
    session.token = response.token
    
    return [decode_timeline_item(item) for item in response.data]


def student_homepage_timeline(session: Session, account: Account) -> list[HomepageTimelineItem]:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request(f"/E/{account.id}/timelineAccueilCommun.awp?verbe=get")
    request.set_token(session.token).set_form_data({})
    
    response = request.send(session.fetcher)
    session.token = response.token
    
    return [decode_homepage_timeline_item(item) for item in response.data.get("postits", [])]


def student_workspace(session: Session, account: Account) -> list[WorkspaceItem]:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request(f"/E/{account.id}/espacestravail.awp?verbe=get")
    request.set_token(session.token).set_form_data({})
    
    response = request.send(session.fetcher)
    session.token = response.token
    
    return [decode_workspace_item(item) for item in response.data or []]


def student_visios(session: Session, account: Account) -> list:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request(f"/eleves/{account.id}/visios.awp?verbe=get")
    request.set_token(session.token).set_form_data({})
    
    response = request.send(session.fetcher)
    session.token = response.token
    
    return response.data


def account_edforms(session: Session, account: Account) -> list:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request("/edforms.awp?verbe=list")
    request.set_token(session.token).set_form_data({
        "idEntity": account.id,
        "typeEntity": account.kind.value
    })
    
    response = request.send(session.fetcher)
    session.token = response.token
    
    return response.data


def student_received_messages(session: Session, account: Account) -> dict:
    if not session.token:
        raise SessionTokenRequired()
    
    current_year = datetime.now().year
    request = Request(f"/eleves/{account.id}/messages.awp?verbe=get&getAll=1")
    request.set_token(session.token).set_form_data({
        "anneeMessages": f"{current_year}-{current_year + 1}"
    })
    
    response = request.send(session.fetcher)
    session.token = response.token
    
    parametrage = response.data.get("parametrage", {})
    can_reply = any([
        parametrage.get("destAdmin", False),
        parametrage.get("destEleve", False),
        parametrage.get("destEspTravail", False),
        parametrage.get("destFamille", False),
        parametrage.get("destProf", False)
    ])
    
    messages = [decode_message_list(m) for m in response.data.get("messages", {}).get("received", [])]
    messages.sort(key=lambda x: x.date, reverse=True)
    
    return {"chats": messages, "can_reply": can_reply}


def read_message(session: Session, account: Account, message_id: int) -> ReceivedMessage:
    if not session.token:
        raise SessionTokenRequired()
    
    request = Request(f"/eleves/{account.id}/messages/{message_id}.awp?verbe=get&mode=destinataire")
    request.set_token(session.token).set_form_data({})
    
    response = request.send(session.fetcher)
    session.token = response.token
    
    data = response.data
    sender_data = data.get("from", {})
    
    try:
        date = datetime.fromisoformat(str(data.get("date", "")))
    except ValueError:
        date = datetime.now()
    
    return ReceivedMessage(
        id=safe_int(data.get("id")),
        type=str(data.get("mtype", "")),
        date=date,
        read=bool(data.get("read", False)),
        subject=str(data.get("subject", "")),
        can_answer=bool(data.get("canAnswer", False)),
        content=decode_string(str(data.get("content", ""))),
        sender=f"{sender_data.get('prenom', '')} {sender_data.get('nom', '')}".strip(),
        files=[{
            "id": f.get("id"),
            "name": str(f.get("libelle", "")),
            "type": FileKind(f.get("type", ""))
        } for f in data.get("files", [])]
    )