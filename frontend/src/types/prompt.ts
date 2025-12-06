export interface PromptTemplate {
  id: string;
  title: string;
  description?: string;
  language: string;
  tags?: string[];
  content: string;
  last_used_at?: string;
  updated_at: string;
}
