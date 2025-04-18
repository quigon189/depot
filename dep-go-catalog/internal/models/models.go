package models

import "time"

type Specialty struct {
	BaseModel
	Code      string `gorm:"size:8;unique;not null"`
	Name      string `gorm:"size:100;unique;not null"`
	ShortName string `gorm:"size:3, not null"`

	Groups []Group `gorm:"foreignKey:SpecID"`
}

type Group struct {
	BaseModel
	Number         uint `gorm:"not null"`
	YearFormed     uint `gorm:"not null"`
	SpecID         uint `gorm:"not null"`
	ClassTeacherID uint

	Students    []Student    `gorm:"foreignKey:GroupID"`
	Disciplines []Discipline `gorm:"foreignKey:GroupID"`
	Teacher     Teacher      `gorm:"foreignKey:ClassTeacherID"`
}

type Student struct {
	BaseModel
	FullName    string    `gorm:"size:255;not null"`
	Birthdate   time.Time `gorm:"not null"`
	PhoneNumber string    `gorm:"size:16"`
	GroupID     uint

	Group Group `gorm:"foreignKey:GroupID"`
}

type Teacher struct {
	BaseModel
	FullName    string    `gorm:"size:255;not null"`
	Birthdate   time.Time `gorm:"not null"`
	PhoneNumber string    `gorm:"size:16"`

	Groups      []Group      `gorm:"foreignKey:ClassTeacherID;"`
	Disciplines []Discipline `gorm:"many2many:teacher_disciplines;"`
}

type Discipline struct {
	BaseModel
	Code     string `gorm:"size:10;not null;"`
	Name     string `gorm:"size:255;not null;"`
	Semester uint   `gorm:"no null;"`
	Hours    uint   `gorm:"no null;"`
	GroupID  uint

	Group    Group       `gorm:"foreignKey:GroupID;"`
	Classes  []Classroom `gorm:"many2many:discipline_classrooms;"`
	Teachers []Teacher   `gorm:"many2many:teacher_disciplines;"`
}

type Classroom struct {
	BaseModel
	Number    uint   `gorm:"no null;"`
	Name      string `gorm:"size:255;no null;"`
	Type      string `gorm:"size:50;"`
	Equipment string `gorm:"type:text;"`
	Capacity  uint
	TeacherID uint

	Teacher     Teacher      `gorm:"foreignKey:TeacherID"`
	Disciplines []Discipline `gorm:"many2many:discipline_classrooms;"`
}
