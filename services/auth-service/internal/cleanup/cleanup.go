package cleanup

import (
	"auth-service/internal/database"
	"context"
	"log"
	"sync"
	"time"
)

type CleanupService struct {
	db       *database.PostgresDB
	wg       sync.WaitGroup
	ctx      context.Context
	cancel   context.CancelFunc
	interval time.Duration
}

func NewCleanupService(db *database.PostgresDB, interval time.Duration) *CleanupService {
	ctx, cancel := context.WithCancel(context.Background())
	return &CleanupService{
		db:       db,
		ctx:      ctx,
		cancel:   cancel,
		interval: interval,
	}
}

func (s *CleanupService) Start() {
	s.wg.Add(1)
	go func() {
		defer s.wg.Done()

		ticker := time.NewTicker(s.interval)
		defer ticker.Stop()

		log.Println("Cleanup service start")

		if err := s.db.DeleteExpiredTokens(); err != nil {
			log.Printf("Failed first cleanup: %v", err)
		}

		for {
			select {
			case <-s.ctx.Done():
				log.Println("Cleanup service stoped")
				return
			case <-ticker.C:
				if err := s.db.DeleteExpiredTokens(); err != nil {
					log.Printf("Failed cleanup: %v", err)
				} 
			}
		}
	}()
}

func (s *CleanupService) Stop() {
	s.cancel()
	s.wg.Wait()
}
