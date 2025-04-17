package models

import "time"

type SpecModel struct {
	BaseModel
	Code string
	Name string
}

type GroupModel struct {
	BaseModel
	Number         uint
	Year           uint
	ClassTeacherID uint
}

type StudentModel struct {
	BaseModel
	FullName    string
	GroupID     uint
	Birthdate   time.Time
	PhoneNumber string
}

type TeacherModel struct {
	BaseModel
	FullName    string
	Birthdate   time.Time
	PhoneNumber string
}

type DisciplineModel struct {
	BaseModel
	Code     string
	Name     string
	GroupID  uint
	Semester uint
	Hours    uint
}

type AudienceModel struct {
	BaseModel
	Number    uint
	Name      string
	TeacherID uint
}
