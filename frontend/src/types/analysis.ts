export interface QualityScore {
  overall_score: number;
  code_quality: number;
  maintainability: number;
  complexity: number;
  duplication: number;
}

export interface Issue {
  issue_type: 'complexity' | 'lint' | 'style' | 'naming';
  severity: 'error' | 'warning' | 'info';
  line_number: number | null;
  column_number: number | null;
  message: string;
  suggestion: string | null;
}

export interface ComplexityMetrics {
  cyclomatic_complexity: number;
  cognitive_complexity: number;
  lines_of_code: number;
  nesting_depth: number;
}

export interface ArchitectureInsight {
  pattern_detected: string;
  confidence: number;
  description: string;
  recommendations: string[];
}

export interface FormattingRecommendation {
  category: string;
  current_style: string;
  recommended_style: string;
  reason: string;
  line_number: number | null;
}

export interface DebugInsight {
  potential_issue: string;
  severity: 'error' | 'warning' | 'info';
  affected_areas: string[];
  debug_steps: string[];
  related_line_numbers: number[];
}

export interface CodeAnalysisRequest {
  code: string;
  language: string;
  file_name?: string;
  analyze_quality?: boolean;
  analyze_issues?: boolean;
  analyze_architecture?: boolean;
  analyze_formatting?: boolean;
}

export interface CodeAnalysisResponse {
  file_name: string | null;
  language: string;
  code_length: number;
  quality_score: QualityScore;
  issues: Issue[];
  complexity_metrics: ComplexityMetrics | null;
  architecture_insights: ArchitectureInsight[];
  formatting_recommendations: FormattingRecommendation[];
  analysis_duration_ms: number;
}

export interface DebugAnalysisResponse {
  file_name: string | null;
  language: string;
  debug_insights: DebugInsight[];
  common_issues: string[];
  analysis_duration_ms: number;
}

export interface SupportedLanguagesResponse {
  supported_languages: string[];
  count: number;
}

export type AnalysisRequest = CodeAnalysisRequest;
export type AnalysisResult = CodeAnalysisResponse;
