"""Tests for code analysis API"""

import pytest


class TestAnalysisEndpoints:
    """Test cases for analysis API endpoints"""

    def test_supported_languages(self, client):
        """Test getting supported languages"""
        response = client.get("/api/analysis/supported-languages")
        assert response.status_code == 200
        data = response.json()
        assert "supported_languages" in data
        assert "count" in data
        assert len(data["supported_languages"]) > 0
        assert "python" in data["supported_languages"]
        assert "javascript" in data["supported_languages"]

    def test_analyze_code_python(self, client):
        """Test analyzing Python code"""
        python_code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

def find_max(items):
    if len(items) == 0:
        return None
    max_item = items[0]
    for item in items[1:]:
        if item > max_item:
            max_item = item
    return max_item
"""
        response = client.post(
            "/api/analysis/analyze",
            json={
                "code": python_code,
                "language": "python",
                "file_name": "test.py",
            },
        )
        assert response.status_code == 200
        data = response.json()

        assert data["language"] == "python"
        assert data["file_name"] == "test.py"
        assert "quality_score" in data
        assert "issues" in data
        assert "complexity_metrics" in data
        assert data["analysis_duration_ms"] > 0

        quality = data["quality_score"]
        assert "overall_score" in quality
        assert "code_quality" in quality
        assert "maintainability" in quality
        assert quality["overall_score"] >= 0 and quality["overall_score"] <= 100

    def test_analyze_code_javascript(self, client):
        """Test analyzing JavaScript code"""
        js_code = """
function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

const processData = (data) => {
    let result = [];
    for (let i = 0; i < data.length; i++) {
        result.push(data[i] * 2);
    }
    return result;
};
"""
        response = client.post(
            "/api/analysis/analyze",
            json={
                "code": js_code,
                "language": "javascript",
                "file_name": "test.js",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "javascript"
        assert "quality_score" in data

    def test_analyze_quality(self, client):
        """Test quality analysis endpoint"""
        code = """
def hello(name):
    return f"Hello, {name}!"
"""
        response = client.post(
            "/api/analysis/analyze/quality",
            json={"code": code, "language": "python"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "quality_score" in data
        quality = data["quality_score"]
        assert "overall_score" in quality
        assert quality["overall_score"] >= 0

    def test_analyze_issues(self, client):
        """Test issue detection endpoint"""
        code = """
def complex_function(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                if x > y:
                    if y > z:
                        if z > 0:
                            return x + y + z
                    else:
                        return x - y
                else:
                    return y - x
            else:
                return z
        else:
            return y
    else:
        return x

very_long_variable_name_that_exceeds_one_hundred_characters_and_should_be_flagged_as_a_style_issue = 42
"""
        response = client.post(
            "/api/analysis/analyze/issues",
            json={"code": code, "language": "python"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "issues" in data
        assert isinstance(data["issues"], list)
        assert len(data["issues"]) > 0

    def test_analyze_complexity(self, client):
        """Test complexity analysis endpoint"""
        code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""
        response = client.post(
            "/api/analysis/analyze/complexity",
            json={"code": code, "language": "python"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "complexity_metrics" in data
        metrics = data["complexity_metrics"]
        assert "cyclomatic_complexity" in metrics
        assert "cognitive_complexity" in metrics
        assert "lines_of_code" in metrics
        assert "nesting_depth" in metrics
        assert metrics["lines_of_code"] > 0

    def test_analyze_architecture(self, client):
        """Test architecture analysis endpoint"""
        code = """
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_instance(self):
        return self
"""
        response = client.post(
            "/api/analysis/analyze/architecture",
            json={"code": code, "language": "python"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "architecture_insights" in data
        assert isinstance(data["architecture_insights"], list)

    def test_analyze_formatting(self, client):
        """Test formatting analysis endpoint"""
        code = """
def format_test():
	x = 10  # Using tab instead of spaces
	return x
"""
        response = client.post(
            "/api/analysis/analyze/formatting",
            json={"code": code, "language": "python"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "formatting_recommendations" in data
        assert isinstance(data["formatting_recommendations"], list)

    def test_analyze_for_debugging(self, client):
        """Test debugging analysis endpoint"""
        code = """
def risky_operation():
    while True:
        data = open('file.txt').read()
        print(data)
    
    result = None
    if result['key'] == 'value':
        pass
"""
        response = client.post(
            "/api/analysis/analyze/debug",
            json={"code": code, "language": "python"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "debug_insights" in data
        assert "common_issues" in data
        assert data["analysis_duration_ms"] > 0

    def test_invalid_language(self, client):
        """Test with invalid language"""
        response = client.post(
            "/api/analysis/analyze",
            json={
                "code": "int x = 5;",
                "language": "cobol",
            },
        )
        assert response.status_code == 400

    def test_empty_code(self, client):
        """Test with empty code"""
        response = client.post(
            "/api/analysis/analyze",
            json={
                "code": "",
                "language": "python",
            },
        )
        assert response.status_code == 422

    def test_analysis_with_file_name(self, client):
        """Test analysis includes file name in response"""
        response = client.post(
            "/api/analysis/analyze",
            json={
                "code": "x = 1",
                "language": "python",
                "file_name": "myfile.py",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["file_name"] == "myfile.py"

    def test_quality_score_ranges(self, client):
        """Test that quality scores are in valid ranges"""
        response = client.post(
            "/api/analysis/analyze/quality",
            json={"code": "x = 1\ny = 2", "language": "python"},
        )
        assert response.status_code == 200
        data = response.json()
        quality = data["quality_score"]

        assert 0 <= quality["overall_score"] <= 100
        assert 0 <= quality["code_quality"] <= 100
        assert 0 <= quality["maintainability"] <= 100
        assert 0 <= quality["complexity"] <= 100
        assert 0 <= quality["duplication"] <= 100

    def test_multiple_issues_detected(self, client):
        """Test detection of multiple issues"""
        code = """
def badly_written_code(a,b,c,d,e,f):
    if a>0:
        if b>0:
            if c>0:
                if d>0:
                    if e>0:
                        if f>0:
                            x=1
                            y=2
                            z=3
                            return x+y+z
    return 0

very_long_line_that_exceeds_one_hundred_characters_for_testing_purposes_and_should_trigger_a_style_issue_warning = 42
"""
        response = client.post(
            "/api/analysis/analyze/issues",
            json={"code": code, "language": "python"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["issues"]) >= 2

    def test_java_code_analysis(self, client):
        """Test analyzing Java code"""
        java_code = """
public class Calculator {
    private static Calculator instance;
    
    private Calculator() {}
    
    public static Calculator getInstance() {
        if (instance == null) {
            instance = new Calculator();
        }
        return instance;
    }
    
    public int add(int a, int b) {
        return a + b;
    }
}
"""
        response = client.post(
            "/api/analysis/analyze",
            json={"code": java_code, "language": "java"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "java"
        assert "quality_score" in data
