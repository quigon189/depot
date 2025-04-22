package services

import (

	"gorm.io/gorm"
)

type GroupService struct {
	*BaseService
	specService *SpecService
}

func NewGroupService(
	db *gorm.DB,
	specService *SpecService,
) *GroupService {
	return &GroupService{
		BaseService: NewBaseService(db),
		specService: specService,
	}
}

// func (s *GroupService) CreateGroup(ctx context.Context, group *models.Group) error {
// 	if _, err := s.specService
// }
