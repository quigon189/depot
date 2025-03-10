package repo

import "testing"

func TestNewUser(t *testing.T) {
	username := "Test"
	pass := "123"
	email := "test@test.com"

	u, err := NewUser(username, email, pass)
	if err != nil {
		t.Error("Error NewUser:", err)
	}

	if !u.CheckPassword(pass) {
		t.Error("Error CheckPassword with correct pass")
	}

	if u.CheckPassword("3213123") {
		t.Error("Error CheckPassword with incorrect pass")
	}
}

func TestRepoAddUser(t *testing.T) {
	name := "test"
	pass := "123"
	email := "test@test.com"
	u, _ := NewUser(name, email, pass)

	r := NewRepo("test.db")
	defer r.Close()
	defer r.db.Exec(DropUsers)

	_, err := r.UserAdd(u)
	if err != nil {
		t.Error("Error Repo.UserAdd:", err)
	}
}

func TestRepoUserGetByName(t *testing.T) {
	name := "test"
	pass := "123"
	email := "test@test.com"
	u, _ := NewUser(name, email, pass)

	r := NewRepo("test.db")
	defer r.Close()
	defer r.db.Exec(DropUsers)

	r.UserAdd(u)

	getUser, err := r.UserGetByName(u.Name)
	if err != nil {
		t.Error("Error GetUserByName:", err)
	}
	if getUser.Name != u.Name {
		t.Error("Error GetUserByName: name don't match")
	}
	t.Logf("%+v --- %+v", u, getUser)
}

func TestRepoUserGetAll(t *testing.T) {
	r := NewRepo("test.db")
	defer r.Close()
	defer r.db.Exec(DropUsers)

	u1, _ := NewUser("Test1", "test@test.com", "123")
	u2, _ := NewUser("Test2", "test2@test.com", "123")
	u3, _ := NewUser("Test3", "t@t.com", "321")
	r.UserAdd(u1)
	r.UserAdd(u2)
	r.UserAdd(u3)

	users, err := r.UserGetAll()
	if err != nil {
		t.Error("Error Repo.UserGetAll:", err)
	}
	if len(users) != 3 {
		t.Error("Error incorrect count users in result")
	}
	t.Log("UserGetAll Tested")
	t.Logf("Result for 3 test users: %+v", users)
}
