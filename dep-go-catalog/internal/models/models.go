package models

type Specialty struct {
	BaseModel
	Code      string `gorm:"size:8;unique;not null" json:"code"`
	Name      string `gorm:"size:100;unique;not null" json:"name"`
	ShortName string `gorm:"size:10, not null" json:"short_name"`

	Groups []Group `gorm:"foreignKey:SpecID" json:"groups"`
}

func (Specialty) TableName() string {
	return "specialties"
}

type Group struct {
	BaseModel
	Number         uint  `gorm:"not null" json:"number"`
	YearFormed     uint  `gorm:"not null" json:"year_formed"`
	SpecID         uint  `gorm:"not null" json:"spec_id"`
	ClassTeacherID *uint `json:"class_teacher_id"`

	Students    []Student    `gorm:"foreignKey:GroupID" json:"students"`
	Disciplines []Discipline `gorm:"foreignKey:GroupID" json:"disciplines"`
	Teacher     *Teacher     `gorm:"foreignKey:ClassTeacherID" json:"class_teacher"`
	Specialty   Specialty    `gorm:"foreignKey:SpecID" json:"specialty"`
}

func (Group) TableName() string {
	return "groups"
}

type Student struct {
	BaseModel
	FirstName   string `gorm:"size:255;not null" json:"first_name"`
	MiddleName  string `gorm:"size:255;not null" json:"middle_name"`
	LastName    string `gorm:"size:255;not null" json:"last_name"`
	BirthDate   string `gorm:"not null" json:"birth_date"`
	PhoneNumber string `gorm:"size:16" json:"phone"`
	GroupID     uint   `json:"group_id"`

	Group Group `gorm:"foreignKey:GroupID" json:"group"`
}

func (Student) TableName() string {
	return "students"
}

type Teacher struct {
	BaseModel
	FirstName   string `gorm:"size:255;not null" json:"first_name"`
	MiddleName  string `gorm:"size:255;not null" json:"middle_name"`
	LastName    string `gorm:"size:255;not null" json:"last_name"`
	BirthDate   string `gorm:"not null" json:"birth_date"`
	PhoneNumber string `gorm:"size:16" json:"phone"`

	Groups      []Group      `gorm:"foreignKey:ClassTeacherID;" json:"groups"`
	Disciplines []Discipline `gorm:"many2many:teacher_disciplines;" json:"disciplines"`
}

func (Teacher) TableName() string {
	return "teachers"
}

type Discipline struct {
	BaseModel
	Code     string `gorm:"size:10;not null;" json:"code"`
	Name     string `gorm:"size:255;not null;" json:"name"`
	Semester uint   `gorm:"no null;" json:"semester"`
	Hours    uint   `gorm:"no null;" json:"hours"`
	GroupID  uint   `json:"group_id"`

	Group    Group       `gorm:"foreignKey:GroupID;" json:"group"`
	Classes  []Classroom `gorm:"many2many:discipline_classrooms;" json:"classess"`
	Teachers []Teacher   `gorm:"many2many:teacher_disciplines;" json:"teachers"`
}

func (Discipline) TableName() string {
	return "disciplines"
}

type Classroom struct {
	BaseModel
	Number    uint   `gorm:"no null;" json:"number"`
	Name      string `gorm:"size:255;no null;" json:"name"`
	Type      string `gorm:"size:50;" json:"type"`
	Equipment string `gorm:"type:text;" json:"Equipment"`
	Capacity  uint   `json:"capacity"`
	TeacherID uint   `json:"teacher_id"`

	Teacher     Teacher      `gorm:"foreignKey:TeacherID" json:"teacher"`
	Disciplines []Discipline `gorm:"many2many:discipline_classrooms;" json:"disciplines"`
}

func (Classroom) TableName() string {
	return "classrooms"
}
