package services

import (
	"dep-go-catalog/internal/models"

	"gorm.io/gorm"
)

type group struct {
	models.Group
}

func (m *group) Validate() error {
	switch {
	case m.Number == 0:
		return ErrInvalidInput
	case m.YearFormed == 0:
		return ErrInvalidInput
	case m.SpecID == 0:
		return ErrInvalidInput
	default:
		return nil
	}
}

type groups []group

func (m *groups) Validate() error {
	return nil
}

type GroupService struct {
	*BaseService
}

func NewGroupService(db *gorm.DB) *GroupService {
	service := &GroupService{BaseService: NewBaseService(db)}
	service.preloads = []string{"Students", "Teacher", "Specialty", "Disciplines"}

	return service
}

func (s *GroupService) NewModel() ServiceModel {
	return &group{}
}

func (s *GroupService) NewModels() ServiceModel {
	return &groups{}
}
//
// func (s *GroupService) CreateGroup(ctx context.Context, group *models.Group) error {
// 	if group.Number == 0 || group.YearFormed == 0 || group.SpecID == 0 {
// 		return ErrInvalidInput
// 	}
// 	if err := s.specService.Get(ctx, s.specService.NewModel(), group.SpecID); err != nil {
// 		switch err {
// 		case ErrNotFound:
// 			return ErrInvalidInput
// 		default:
// 			return err
// 		}
// 	}
//
// 	if group.ClassTeacherID != nil {
// 		if _, err := s.teacherService.GetTeacher(ctx, *group.ClassTeacherID); err != nil {
// 			switch err {
// 			case ErrNotFound:
// 				return ErrInvalidInput
// 			default:
// 				return err
// 			}
// 		}
// 	}
//
// 	return s.db.WithContext(ctx).Create(&group).Error
// }
//
// func (s *GroupService) GetGroup(ctx context.Context, id uint) (*models.Group, error) {
// 	var group models.Group
//
// 	err := s.db.WithContext(ctx).
// 		Preload("Students").
// 		Preload("Disciplines").
// 		Preload("Teacher").
// 		First(&group, "id = ?", id).Error
//
// 	switch {
// 	case errors.Is(err, gorm.ErrRecordNotFound):
// 		return nil, ErrNotFound
// 	case err != nil:
// 		return nil, err
// 	}
//
// 	return &group, nil
// }
//
// func (s *GroupService) GetAllGroup(ctx context.Context) ([]models.Group, error) {
// 	var groups []models.Group
//
// 	err := s.db.WithContext(ctx).
// 		Preload("Students").
// 		Preload("Disciplines").
// 		Preload("Teacher").
// 		Find(&groups).Error
//
// 	if err != nil {
// 		return nil, err
// 	}
//
// 	return groups, nil
// }
