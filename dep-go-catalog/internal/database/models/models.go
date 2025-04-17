package models

import "time"

type Specialty struct {
	BaseModel
	Code      string  `gorm:"size:8"`
	Name      string  `gorm:"size:100"`
	ShortName string  `gorm:"size:3"`
	Groups    []Group `gorm:"foreignKey:SpecID"`
}

type Group struct {
	BaseModel
	Number         uint
	Year           uint
	ClassTeacherID uint
	SpecID         uint
	Students       []Student `gorm:"foreignKey:GroupID"`
	Disciplines 
}

type Student struct {
	BaseModel
	FullName    string
	GroupID     uint
	Birthdate   time.Time
	PhoneNumber string
}

type Teacher struct {
	BaseModel
	FullName    string
	Birthdate   time.Time
	PhoneNumber string
}

type Discipline struct {
	BaseModel
	Code     string
	Name     string
	GroupID  uint
	Semester uint
	Hours    uint
}

type Audience struct {
	BaseModel
	Number    uint
	Name      string
	TeacherID uint
}
