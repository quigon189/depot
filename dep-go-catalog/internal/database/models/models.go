mackage models

import "time"

type Specialty struct {
	BaseModel
	Code      string  `gorm:"size:8;unique;no null"`
	Name      string  `gorm:"size:100;unique;no null"`
	ShortName string  `gorm:"size:3, no null"`
	Groups    []Group `gorm:"foreignKey:SpecID"`
}

type Group struct {
	BaseModel
	Number         uint `gorm:"no null"`
	Year           uint `gorm:"no null"`
	ClassTeacherID uint
	SpecID         uint         `gorm:"no null"`
	Students       []Student    `gorm:"foreignKey:GroupID"`
	Disciplines    []Discipline `gorm:"foreignKey:GroupID"`
}

type Student struct {
	BaseModel
	FullName    string `gorm:"size:255;no null"`
	GroupID     uint
	Birthdate   time.Time `gorm:"no null"`
	PhoneNumber string    `gorm:"size:16"`
}

type Teacher struct {
	BaseModel
	FullName    string    `gorm:"size:255;no null"`
	Birthdate   time.Time `gorm:"no null"`
	PhoneNumber string    `gorm:"size:16"`
}

type Discipline struct {
	BaseModel
	Code     string `gorm:"size:10;no null"`
	Name     string `gorm:"size:255;no null"`
	GroupID  uint
	Semester uint `gorm:"no null"`
	Hours    uint `gorm:"no null"`
}

type Audience struct {
	BaseModel
	Number    uint `gorm:"no null"`
	Name      string `gorm:"size:255;no null"`
	TeacherID uint
}
