import api from '@/lib/api'

export const taskApi = {
  // Get tasks for the current intern's assigned project only
  getMyTasks: () => api.get('/api/tasks/my-tasks'),

  // Get active sprint for current intern's project
  getActiveSprints: () => api.get('/api/tasks/sprints/active'),

  // Get a single task
  getTask: (id) => api.get(`/api/tasks/${id}`),

  // Update task status
  updateTaskStatus: (id, status) => api.patch(`/api/tasks/${id}/status`, { status }),

  // Update full task
  updateTask: (id, data) => api.patch(`/api/tasks/${id}`, data),
}
