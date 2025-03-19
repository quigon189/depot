package repo

import "testing"

func TestNewUser(t *testing.T) {
	username := "Test"
	pass := "123123123"
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
	pass := "123123123"
	email := "test@test.com"
	u, _ := NewUser(name, email, pass)

	userRepo := NewUserRepo("test.db")
	defer userRepo.Close(true)

	_, err := userRepo.Add(u)
	if err != nil {
		t.Error("Error UserRepo.Add:", err)
	}
}

func TestRepoUserGetByName(t *testing.T) {
	name := "test"
	pass := "123123123"
	email := "test@test.com"
	u, _ := NewUser(name, email, pass)

	userRepo := NewUserRepo("test.db")
	defer userRepo.Close(true)

	userRepo.Add(u)

	getUser, err := userRepo.GetByName(u.Name)
	if err != nil {
		t.Error("Error GetUserByName:", err)
	}
	if getUser.Name != u.Name {
		t.Error("Error GetUserByName: name don't match")
	}
	t.Logf("%+v --- %+v", u, getUser)
}

func TestRepoUserGetAll(t *testing.T) {
	userRepo := NewUserRepo("test.db")
	defer userRepo.Close(true)

	u1, _ := NewUser("Test1", "test@test.com", "123123123")
	u2, _ := NewUser("Test2", "test2@t.com", "123123123j")
	u3, _ := NewUser("Test3", "t@t.com", "32112312312")
	userRepo.Add(u1)
	userRepo.Add(u2)
	userRepo.Add(u3)

	users, err := userRepo.GetAll()
	if err != nil {
		t.Error("Error Repo.UserGetAll:", err)
	}
	if len(users) != 3 {
		t.Error("Error incorrect count users in result")
	}
	t.Logf("Result for 3 test users: %+v", users)
}
