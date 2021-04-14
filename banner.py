import requests
import re
import time

from dataclasses import dataclass
from typing import List
from enum import IntEnum

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

class TermDesc(IntEnum):
    FALL_SEMESTER = 110
    FALL_LAW_SEMESTER = 112
    FALL_CPS_SEMESTER = 114
    FALL_CPS_QUARTER = 115
    FALL_LAW_QUARTER = 118
    WINTER_CPS_QUARTER = 25
    WINTER_LAW_QUARTER = 28
    SPRING_SEMESTER = 30
    SPRING_LAW_SEMESTER = 32
    SPRING_CPS_SEMESTER = 34
    SPRING_CPS_QUARTER = 35
    SPRING_LAW_QUARTER = 38
    SUMMER_1_SEMESTER = 40
    SUMMER_FULL_SEMESTER = 50
    SUMMER_SEMESTER_LAW = 52
    SUMMER_CPS_SEMESTER = 54
    SUMMER_CPS_QUARTER = 55
    SUMMER_LAW_QUARTER = 58
    SUMMER_2_SEMESTER = 60

@dataclass
class Term:
    year: int
    termDesc: TermDesc

    def getCode(self):
        return self.year * 100 + self.termDesc
    
    def __lt__(self, other):
        return self.getCode() < other.getCode()

    @staticmethod
    def fromCode(code):
        for desc in TermDesc:
            if (code - desc) % 100 == 0:
                return Term((code - desc) // 100, desc)

@dataclass
class BannerQuery:
    term: Term
    subject: str = ''
    courseNumber: int = 0
    sequenceNumber: str = ''
    pageMaxSize: int = 100

    def getParams(self):
        params = {
            "txt_term": self.term.getCode(),
            "pageMaxSize": self.pageMaxSize
        }

        if self.courseNumber:
            params['txt_courseNumber'] = self.courseNumber
            
        if self.subject:
            params['txt_subject'] = self.subject
        
        if self.pageMaxSize != BannerQuery.pageMaxSize:
            params['pageMaxSize'] = self.pageMaxSize
        
        return params

""" ------------------------------- Banner functions ------------------------------- """

j = re.compile('JSESSIONID=[0-9A-F]*;')
n = re.compile('nubanner-cookie=[0-9\.]*;')

MIN_TERM = Term(2009, TermDesc.FALL_SEMESTER) # Fall of 2009

def validateSession(term):
    headers = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UT' }
    data = f'term={term.getCode()}&studyPath=&studyPathText=&startDatepicker=&endDatepicker='

    res = requests.post('https://nubanner.neu.edu/StudentRegistrationSsb/ssb/term/search?mode=plan', headers=headers, data=data)

    set_cookie = res.headers['set-cookie']

    return j.search(set_cookie).group() + n.search(set_cookie).group()

def searchCourses(query: BannerQuery) -> BannerResult:
    if query.term < MIN_TERM:
        raise Exception(f'Minimum term is Fall of 2009 ({MIN_TERM})')

    cookie = validateSession(query.term)

    headers = { 'Cookie': cookie }
    # Reset the form before sending query
    reset = requests.post('https://nubanner.neu.edu/StudentRegistrationSsb/ssb/classSearch/resetDataForm', headers=headers)

    # Send query request and get result
    res = requests.get('https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults', headers=headers, params=query.getParams())

    return BannerResult.fromJSON(res.json())
