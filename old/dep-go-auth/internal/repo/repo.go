package repo

type Repo interface {
	Add(u *User) (int, error)
	GetByName(name string) (*User, error)
	Close(drop bool) 
}
