import api from './api';

export interface AnalyzeResponse {
  api_name: string;
  version: string;
  endpoint_count: number;
  analysis: {
    endpoint_summary: any[];
    auth_methods: string[];
    data_formats: any;
    required_transformations: any[];
  };
}

export interface GenerateResponse {
  project_id: string;
  message: string;
  api_name: string;
  endpoint_count: number;
  framework: string;
  target_standard: string;
}

export const analyzeApiSpec = async (file: File): Promise<AnalyzeResponse> => {
  const formData = new FormData();
  formData.append('api_spec', file);

  const response = await api.post('/parser/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const generateMiddleware = async (
  file: File,
  framework: string,
  targetStandard: string
): Promise<GenerateResponse> => {
  const formData = new FormData();
  formData.append('api_spec', file);
  formData.append('framework', framework);
  formData.append('target_standard', targetStandard);

  const response = await api.post('/middleware/generate', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const getDownloadUrl = (projectId: string): string => {
  return `/api/middleware/download/${projectId}`;
};