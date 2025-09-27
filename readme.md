# PyDirecte

A Python API wrapper for EcoleDirecte - Access your school data programmatically.

[![PyPI version](https://badge.fury.io/py/pydirecte.svg)](https://badge.fury.io/py/pydirecte)
[![Python Support](https://img.shields.io/pypi/pyversions/pydirecte.svg)](https://pypi.org/project/pydirecte/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Features

- 🔐 **Authentication** - Login with username/password, handle double authentication
- 📚 **Grades** - Retrieve grades, averages, and subject overviews
- 📝 **Homework** - Get homework assignments, mark them as done/undone
- 📅 **Timetable** - Access your school schedule
- 📧 **Messages** - Read received messages
- 📄 **Documents** - Download school documents
- 🍽️ **Canteen** - Check canteen reservations and barcodes
- 👤 **School Life** - View absences, delays, and sanctions
- 🌐 **Timeline** - Get school news and updates
- 💼 **Workspaces** - Access collaborative workspaces

## Installation

```bash
pip install pydirecte
```

## Quick Start

```python
from pydirecte import Session, login, set_access_token, student_grades

session = Session(
    username="your_username",
    device_uuid="your-secure-device-uuid"
)

accounts = login(session, "your_password")
account = accounts[0]

set_access_token(session, account)

grades_data = student_grades(session, account)
print(f"Found {len(grades_data['grades'])} grades")
```

## Authentication

### Basic Login

```python
from pydirecte import Session, login, set_access_token

session = Session(
    username="student_username",
    device_uuid="unique-device-identifier"
)

try:
    accounts = login(session, "password")
    account = accounts[0]
    set_access_token(session, account)
    
    print(f"Logged in as {account.first_name} {account.last_name}")
    print(f"School: {account.school_name}")
    print(f"Class: {account.class_long}")
except Exception as e:
    print(f"Login failed: {e}")
```

### Double Authentication

When double authentication is required:

```python
from pydirecte import (
    Session, login, init_double_auth, 
    check_double_auth, DoubleAuthRequired
)

session = Session(username="username", device_uuid="device-uuid")

try:
    accounts = login(session, "password")
except DoubleAuthRequired:
    challenge = init_double_auth(session)
    
    print(f"Question: {challenge.question}")
    for i, answer in enumerate(challenge.answers):
        print(f"[{i}] {answer}")
    
    answer_index = int(input("Select answer: "))
    selected_answer = challenge.answers[answer_index]
    
    if check_double_auth(session, selected_answer):
        print("Double auth confirmed!")
        accounts = login(session, "password")
```

### Session Refresh

```python
from pydirecte import refresh, AccountKind

accounts = refresh(session, AccountKind.STUDENT)
account = accounts[0]
```

## Grades

### Get All Grades

```python
from pydirecte import student_grades

grades_data = student_grades(session, account)

for grade in grades_data['grades']:
    print(f"{grade.subject.name}: {grade.value.points}/{grade.out_of}")
    print(f"Average: {grade.average.points}")
    print(f"Date: {grade.date}")
    print(f"Comment: {grade.comment}")
```

### Get Grades for Specific Year

```python
grades_data = student_grades(session, account, year="2023")
```

### Access Grades Overview

```python
overview = grades_data['overview']

for period_id, period_overview in overview.items():
    print(f"Period: {period_id}")
    print(f"Overall Average: {period_overview.overall_average.points}")
    print(f"Class Average: {period_overview.class_average.points}")
    
    for subject in period_overview.subjects:
        print(f"  {subject.name}: {subject.student_average.points}/20")
```

### Periods

```python
for period in grades_data['periods']:
    print(f"{period.name}: {period.start_date} to {period.end_date}")
    print(f"Ended: {period.is_ended}")
```

## Homework

### Get Homework for Specific Date

```python
from pydirecte import student_homeworks

homework_data = student_homeworks(session, account, "2024-12-15")

for hw in homework_data['homeworks']:
    print(f"Subject: {hw.subject}")
    print(f"Teacher: {hw.teacher}")
    print(f"Done: {hw.done}")
    print(f"Content: {hw.content}")
    print(f"Exam: {hw.exam}")
```

### Get Coming Homework

```python
from pydirecte import student_coming_homeworks

coming = student_coming_homeworks(session, account)

for day in coming:
    print(f"Date: {day['date']}")
    for hw in day['homeworks']:
        print(f"  - {hw.subject} (Done: {hw.done})")
```

### Mark Homework as Done/Undone

```python
from pydirecte import set_homework_state

set_homework_state(session, account, homework_id=12345, done=True)
```

## Timetable

```python
from pydirecte import student_timetable
from datetime import datetime

start_date = datetime(2024, 12, 16)
timetable = student_timetable(session, account, start_date)

for item in timetable:
    print(f"{item.start_date.strftime('%H:%M')} - {item.end_date.strftime('%H:%M')}")
    print(f"Subject: {item.subject_name}")
    print(f"Room: {item.room}")
    print(f"Teacher: {item.teacher}")
    print(f"Cancelled: {item.cancelled}")
```

### Get Week Timetable

```python
from datetime import datetime, timedelta

start_date = datetime(2024, 12, 16)
end_date = start_date + timedelta(days=6)

timetable = student_timetable(session, account, start_date, end_date)
```

## Messages

### List Received Messages

```python
from pydirecte import student_received_messages

messages_data = student_received_messages(session, account)

print(f"Can reply: {messages_data['can_reply']}")

for msg in messages_data['chats']:
    print(f"[{msg.id}] From: {msg.sender}")
    print(f"Subject: {msg.subject}")
    print(f"Date: {msg.date}")
    print(f"Read: {msg.read}")
```

### Read Specific Message

```python
from pydirecte import read_message

message = read_message(session, account, message_id=12345)

print(f"From: {message.sender}")
print(f"Subject: {message.subject}")
print(f"Content: {message.content}")

for file in message.files:
    print(f"Attachment: {file['name']} ({file['type']})")
```

### Download Message Attachment

```python
from pydirecte import get_file

response = get_file(session, file['type'], file['id'])

with open(file['name'], 'wb') as f:
    f.write(response.content)
```

## Documents

### List All Documents

```python
from pydirecte import student_documents

documents = student_documents(session)

for doc in documents:
    print(f"[{doc.id}] {doc.name}")
    print(f"Date: {doc.date}")
    print(f"Type: {doc.kind}")
    print(f"Signature required: {doc.signature_required}")
```

### Download Document

```python
from pydirecte import get_file, FileKind

response = get_file(session, FileKind.DOCUMENT, document_id)

with open("document.pdf", "wb") as f:
    f.write(response.content)
```

## School Life

### View Attendance Issues

```python
from pydirecte import student_attendance

attendance = student_attendance(session, account)

print(f"Absences: {len(attendance['absences'])}")
for absence in attendance['absences']:
    print(f"  - {absence.date}: {absence.label}")
    print(f"    Justified: {absence.justified}")

print(f"Delays: {len(attendance['punishments'])}")
for delay in attendance['punishments']:
    print(f"  - {delay.date}: {delay.reason}")
```

## Canteen

```python
from pydirecte import student_cantine

cantine = student_cantine(account)

if 'reservation' in cantine:
    meals = cantine['reservation'].meals
    print(f"Monday lunch: {meals['monday'].lunch}")
    print(f"Diet: {cantine['reservation'].diet}")

if 'barcode' in cantine:
    print(f"Badge number: {cantine['barcode'].badge_number}")
```

## Timeline & News

### Student Timeline

```python
from pydirecte import student_timeline

timeline = student_timeline(session, account)

for item in timeline:
    print(f"[{item.element_kind}] {item.title}")
    print(f"Date: {item.date}")
    print(f"Content: {item.content}")
```

### Homepage Timeline

```python
from pydirecte import student_homepage_timeline

homepage = student_homepage_timeline(session, account)

for item in homepage:
    print(f"{item.author_name}: {item.content}")
    print(f"From {item.start_date} to {item.end_date}")
```

## Workspaces

```python
from pydirecte import student_workspace

workspaces = student_workspace(session, account)

for ws in workspaces:
    print(f"[{ws.id}] {ws.title}")
    print(f"Description: {ws.description}")
    print(f"Members: {ws.nb_members}")
    print(f"Is member: {ws.is_member}")
    print(f"Is admin: {ws.is_admin}")
```

## Error Handling

```python
from pydirecte import (
    BadCredentials,
    DoubleAuthRequired,
    InvalidVersion,
    SessionTokenRequired
)

try:
    accounts = login(session, "password")
except BadCredentials:
    print("Invalid username or password")
except DoubleAuthRequired:
    print("Double authentication is required")
except InvalidVersion:
    print("API version is outdated")
except SessionTokenRequired:
    print("Session token is required for this operation")
```

## Advanced Usage

### Custom HTTP Client

```python
def custom_fetcher(request):
    import requests
    response = requests.post(
        request.url,
        params=request.params,
        headers=request.headers,
        data=request.content,
        timeout=30
    )
    return response

session = Session(
    username="username",
    device_uuid="device-uuid",
    fetcher=custom_fetcher
)
```

### File Downloads

```python
from pydirecte import FileKind, get_file

homework_file = get_file(session, FileKind.HOMEWORK, file_id)

with open("homework.pdf", "wb") as f:
    f.write(homework_file.content)
```

## Data Models

### Account

```python
@dataclass
class Account:
    login_id: int
    id: int
    user_id: str
    username: str
    kind: AccountKind
    first_name: str
    last_name: str
    email: str
    school_name: str
    class_short: str
    class_long: str
```

### Grade

```python
@dataclass
class Grade:
    value: GradeValue
    out_of: float
    average: GradeValue
    max_value: GradeValue
    min_value: GradeValue
    coefficient: float
    subject: Subject
    date: datetime
    comment: str
```

### GradeValue

```python
@dataclass
class GradeValue:
    kind: GradeKind  # GRADE, ABSENT, EXEMPTED, NOT_GRADED, WAITING
    points: float
```

## Enumerations

### AccountKind
- `STUDENT = "E"`

### GradeKind
- `ERROR = -1`
- `GRADE = 0`
- `ABSENT = 1`
- `EXEMPTED = 2`
- `NOT_GRADED = 3`
- `WAITING = 4`

### FileKind
- `CLOUD = "CLOUD"`
- `HOMEWORK = "FICHIER_CDT"`
- `ATTACHMENT = "PIECE_JOINTE"`
- `CANTINE_MENU = "FICHIER_MENU_RESTAURATION"`
- `ADMINISTRATIVE = "ADMINISTRATIF"`

### DocumentKind
- `GRADES = "Note"`
- `DOCUMENT = "Doc"`
- `SCHOOL_LIFE = "Viesco"`
- `INVOICE = "Fac"`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 or later - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is an unofficial API wrapper for EcoleDirecte. Use at your own risk. The authors are not responsible for any misuse of this library.

## Author

**kikkopy** - [GitHub](https://github.com/kikkopy)

## Acknowledgments

Inspired by [Pawdirecte](https://github.com/LiterateInk/Pawdirecte) - The TypeScript version of this wrapper.

## Support

For bugs and feature requests, please [open an issue](https://github.com/kikkopy/pydirecte/issues).
