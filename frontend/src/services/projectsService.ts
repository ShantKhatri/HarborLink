import api from './api';

export interface Project {
  id: string;
  api_name: string;
  framework: string;
  target_standard: string;
  created_at: string;
  updated_at: string;
  generated_code?: Record<string, string>;
}

export const getProjects = async (): Promise<Project[]> => {
  const response = await api.get('/projects');
  return response.data;
};

export const getProject = async (id: string): Promise<Project> => {
  const response = await api.get(`/projects/${id}`);
  return response.data;
};