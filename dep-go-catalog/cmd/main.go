package main

import (
	"context"
	"dep-go-catalog/internal/config"
	"dep-go-catalog/internal/database"
	"dep-go-catalog/internal/models"
	"dep-go-catalog/internal/services"

	"log"

	"gorm.io/gorm"
)

func AddTestSpec(db *gorm.DB) error {
	spec := models.Specialty{
		Code:      "12.34.56",
		Name:      "asdasd",
		ShortName: "as",
	}
	SpecService := services.NewSpecService(db)

	err := SpecService.CreateSpec(context.Background(), &spec)
	if err != nil {
		log.Fatal(err)
	}

	rspec, err := SpecService.GetWithGroup(context.Background(), "12.34.56")
	if err != nil {
		log.Fatal(err)
	}

	log.Printf("%+v", rspec)
	return nil
}

func main() {
	cfg := config.FetchConfig()
	log.Printf("%+v", cfg)

	db := database.Connect(cfg)
	database.AutoMigrate(db)

	err := AddTestSpec(db)
	if err != nil {
		log.Fatal(err)
	}

	log.Fatalf("server %s:%s stoped", cfg.Server.Host, cfg.Server.Port)
}
