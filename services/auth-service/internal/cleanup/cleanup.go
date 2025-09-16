package cleanup

import (
	"context"
	"database/sql"
	"log"
	"sync"
	"time"
)

type CleanupService struct {
	db       *sql.DB
	wg       sync.WaitGroup
	ctx      context.Context
	cancel   context.CancelFunc
	interval time.Duration
}

func NewCleanupService(db *sql.DB, interval time.Duration) *CleanupService {
	ctx, cancel := context.WithCancel(context.Background())
	return &CleanupService{
		db: db,
		ctx: ctx,
		cancel: cancel,
		interval: interval,
	}
}

func (s *CleanupService) DeleteExpiredTokens() error {
	query := `DELETE FROM refresh_tokens WHERE expires_at < NOW()`
	result, err := s.db.Exec(query)
	if err != nil {
		return err
	}

	rowsAffected, _ := result.RowsAffected()
	if rowsAffected > 0 {
		log.Printf("Deleted expired tokens: %d", rowsAffected)
	}

	return nil
} 
