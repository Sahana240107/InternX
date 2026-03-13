import api from '@/lib/api'

export const taskApi = {
  // Sprints
  getSprints:        ()                    => api.get('/api/tasks/sprints'),
  getActiveSprints:  ()                    => api.get('/api/tasks/sprints/active'),
  getSprintProgress: (id)                  => api.get(`/api/tasks/sprints/${id}/progress`),
  createSprint:      (data)                => api.post('/api/tasks/sprints', data),

  // Tasks
  getMyTasks:        ()                    => api.get('/api/tasks/my'),
  getSprintTasks:    (sprintId)            => api.get(`/api/tasks/sprint/${sprintId}`),
  getTask:           (id)                  => api.get(`/api/tasks/${id}`),
  createTask:        (data)                => api.post('/api/tasks/', data),
  updateStatus:      (id, status)          => api.put(`/api/tasks/${id}/status`, { status }),
  submitPR:          (id, pr_url)          => api.put(`/api/tasks/${id}/submit`, { pr_url }),
  scoreTask:         (id, score, feedback) => api.put(`/api/tasks/${id}/score`, { score, feedback }),
  getLeaderboard:    (sprintId)            => api.get(`/api/tasks/leaderboard/${sprintId}`),
}