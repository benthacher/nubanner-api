import requests
import re
import time

from dataclasses import dataclass
from typing import List

""" ------------------------------- Banner Data classes ------------------------------- """

@dataclass
class Faculty:
    bannerId: int = 0
    category: str = ''
    _class: str = ''
    courseReferenceNumber: int = 0
    displayName: str = ''
    emailAddress: str = ''
    primaryIndicator: bool = False
    term: int = 0

    __special_keys = [ '_class' ]

    @staticmethod
    def fromJSON(json):
        if not json:
            return None

        res = Faculty()

        for key in json.keys():
            if key in vars(res) and not key in Faculty.__special_keys:
                setattr(res, key, json[key])
        
        res._class = json['class']

        return res

@dataclass
class Status:
    select: bool = False
    sectionOpen: bool = False
    timeConflict: bool = False
    restricted: bool = False
    sectionStatus: bool = False

    @staticmethod
    def fromJSON(json):
        if not json:
            return None

        res = Status()

        for key in json.keys():
            if key in vars(res):
                setattr(res, key, json[key])
        
        return res

@dataclass
class SectionAttribute:
    _class: str = ''
    code: str = ''
    courseReferenceNumber: int = 0
    description: str = ''
    isZTCAttribute: bool = False
    termCode: int = 0

    __special_keys = [ '_class' ]

    @staticmethod
    def fromJSON(json):
        if not json:
            return None
            
        res = SectionAttribute()

        for key in json.keys():
            if key in vars(res) and not key in SectionAttribute.__special_keys:
                setattr(res, key, json[key])
        
        res._class = json['class']

        return res

@dataclass
class MeetingTime:
    beginTime: int = 0
    building: str = ''
    buildingDescription: str = ''
    campus: str = ''
    campusDescription: str = ''
    category: str = ''
    _class: str = ''
    courseReferenceNumber: int = 0
    creditHourSession: float = 0.0
    days: List[str] = None # This property is generated in the fromJSON static method and is not part of the response JSON
    endDate: str = ''
    endTime: int = 0
    friday: bool = False
    hoursWeek: float = 0.0
    meetingScheduleType: str = ''
    meetingType: str = ''
    meetingTypeDescription: str = ''
    monday: bool = False
    room: str = ''
    saturday: bool = False
    startDate: str = ''
    sunday: bool = False
    term: int = 0
    thursday: bool = False
    tuesday: bool = False
    wednesday: bool = False

    __special_keys = [ '_class', 'days' ]
    __days = [ 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]

    @staticmethod
    def fromJSON(json):
        if not json:
            return None

        res = MeetingTime()

        for key in json.keys():
            if key in vars(res) and not key in MeetingTime.__special_keys:
                setattr(res, key, json[key])
        
        res._class = json['class']
        res.days = [day for day in MeetingTime.__days if getattr(res, day)]

        return res

@dataclass
class MeetingsFaculty:
    category: int = 0
    _class: str = ''
    courseReferenceNumber: int = 0
    faculty: List[Faculty] = None
    meetingTime: MeetingTime = None
    term: int = 0

    __special_keys = [ '_class', 'faculty', 'meetingTime' ]

    @staticmethod
    def fromJSON(json):
        if not json:
            return None

        res = MeetingsFaculty()

        for key in json.keys():
            if key in vars(res) and not key in MeetingsFaculty.__special_keys:
                setattr(res, key, json[key])
        
        res._class = json['class']
        res.faculty = []

        for faculty in json['faculty']:
            res.faculty.append(Faculty.fromJSON(faculty))

        res.meetingTime = MeetingTime.fromJSON(json['meetingTime'])

        return res

@dataclass
class BannerClass:
    id: int = 0
    term: int = 0
    termDesc: str = ''
    courseReferenceNumber: int = 0
    partOfTerm: int = 0
    courseNumber: int = 0
    subject: str = ''
    subjectDescription: str = ''
    sequenceNumber: str = ''
    campusDescription: str = ''
    scheduleTypeDescription: str = ''
    courseTitle: str = ''
    creditHours: str = ''
    maximumEnrollment: int = 0
    enrollment: int = 0
    seatsAvailable: int = 0
    waitCapacity: int = 0
    waitCount: int = 0
    waitAvailable: int = 0
    crossList: str = ''
    crossListCapacity: int = 0
    crossListCount: int = 0
    crossListAvailable: bool = False
    creditHourHigh: int = 0
    creditHourLow: int = 0
    creditHourIndicator: str = ''
    openSection: bool = False
    linkIdentifier: str = ''
    isSectionLinked: bool = False
    subjectCourse: str = ''
    faculty: List[Faculty] = None
    meetingsFaculty: List[MeetingsFaculty] = None
    status: Status = None
    reservedSeatSummary: str = ''
    sectionAttributes: List[SectionAttribute] = None

    __special_keys = [ 'faculty', 'meetingsFaculty', 'status', 'sectionAttributes' ]

    @staticmethod
    def fromJSON(json):
        if not json:
            return None

        res = BannerClass()

        for key in json.keys():
            if key in vars(res) and not key in BannerClass.__special_keys:
                setattr(res, key, json[key])
        
        res.faculty = []
        res.meetingsFaculty = []
        res.sectionAttributes = []

        res.status = Status.fromJSON(json['status'])

        for faculty in json['faculty']:
            res.faculty.append(Faculty.fromJSON(faculty))

        for meetingsFaculty in json['meetingsFaculty']:
            res.meetingsFaculty.append(MeetingsFaculty.fromJSON(meetingsFaculty))

        for sectionAttributes in json['sectionAttributes']:
            res.sectionAttributes.append(SectionAttribute.fromJSON(sectionAttributes))

        return res

@dataclass
class SearchResultsConfig:
    config: str = ''
    display: str = ''
    title: str = ''
    width: str = ''

    @staticmethod
    def fromJSON(json):
        if not json:
            return None

        res = SearchResultsConfig()

        for key in json.keys():
            if key in vars(res):
                setattr(res, key, json[key])

        return res

@dataclass
class BannerResult:
    success: bool = False
    totalCount: int = 0
    data: List[BannerClass] = None
    pageOffset: int = 0
    pageMaxSize: int = 0
    sectionsFetchedCount: int = 0
    pathMode: str = ''
    searchResultsConfigs: List[SearchResultsConfig] = None
    ztcEncodedImage: str = ''

    __special_keys = [ 'data', 'searchResultsConfigs' ]

    @staticmethod
    def fromJSON(json):
        if not json:
            return None

        res = BannerResult()

        for key in json.keys():
            # Set primitive data
            if key in vars(res) and not key in BannerResult.__special_keys:
                setattr(res, key, json[key])
        
        res.searchResultsConfigs = []
        res.data = []
        
        for config in json['searchResultsConfigs']:
            res.searchResultsConfigs.append(SearchResultsConfig.fromJSON(config))

        for classData in json['data']:
            res.data.append(BannerClass.fromJSON(classData))
        
        return res

@dataclass
class BannerQuery:
    subject: str = ''
    courseNumber: int = 0
    sequenceNumber: str = None
    pageMaxSize: int = 100
    term: int = 0

    __params = {
        "subject": "txt_subject",
        "courseNumber": "txt_courseNumber",
        "term": "txt_term",
        "pageMaxSize": "pageMaxSize",
    }

    def getParams(self):
        params = {}

        for key, value in BannerQuery.__params.items():
            attr = getattr(self, key)

            if attr != getattr(BannerQuery, key): # If attribute is not equal to the default value, add it to the params dict
                params[value] = getattr(self, key)

""" ------------------------------- Banner functions ------------------------------- """

j = re.compile('JSESSIONID=[0-9A-F]*;')
n = re.compile('nubanner-cookie=[0-9\.]*;')

def validateSession(term):
    headers = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UT' }
    data = f'term={term}&studyPath=&studyPathText=&startDatepicker=&endDatepicker='

    res = requests.post('https://nubanner.neu.edu/StudentRegistrationSsb/ssb/term/search?mode=plan', headers=headers, data=data)

    set_cookie = res.headers['set-cookie']

    return j.search(set_cookie).group() + n.search(set_cookie).group()

def searchCourses(query: BannerQuery, term, cookie) -> BannerResult:
    headers = { 'Cookie': cookie }
    reset = requests.post('https://nubanner.neu.edu/StudentRegistrationSsb/ssb/classSearch/resetDataForm', headers=headers)

    res = requests.get('https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults', headers=headers, params=query.getParams())

    json = res.json()

    return BannerResult.fromJSON(json)
