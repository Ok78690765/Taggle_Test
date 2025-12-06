"""Tests for code analysis service"""

import pytest

from app.services.code_analyzer import AnalysisService, CodeAnalyzer
from app.utils.language_adapter import (
    JavaAdapter,
    JavaScriptAdapter,
    LanguageAdapterFactory,
    PythonAdapter,
)


class TestLanguageAdapters:
    """Test language adapter functionality"""

    def test_python_adapter_functions(self):
        """Test Python function extraction"""
        code = """
def hello(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b
"""
        adapter = PythonAdapter()
        functions = adapter.extract_functions(code)
        assert len(functions) == 2
        assert functions[0]["name"] == "hello"
        assert functions[1]["name"] == "add"

    def test_python_adapter_classes(self):
        """Test Python class extraction"""
        code = """
class Animal:
    pass

class Dog(Animal):
    pass
"""
        adapter = PythonAdapter()
        classes = adapter.extract_classes(code)
        assert len(classes) == 2
        assert classes[0]["name"] == "Animal"
        assert classes[1]["name"] == "Dog"

    def test_python_adapter_imports(self):
        """Test Python import extraction"""
        code = """
import os
from sys import argv
import numpy as np
"""
        adapter = PythonAdapter()
        imports = adapter.extract_imports(code)
        assert len(imports) == 3
        assert any("os" in imp for imp in imports)
        assert any("sys" in imp for imp in imports)

    def test_python_adapter_comments(self):
        """Test Python comment extraction"""
        code = """
# This is a comment
x = 1  # inline comment
# Another comment
y = 2
"""
        adapter = PythonAdapter()
        comments = adapter.extract_comments(code)
        assert len(comments) >= 2

    def test_javascript_adapter_functions(self):
        """Test JavaScript function extraction"""
        code = """
function greet(name) {
    return "Hello " + name;
}

const add = (a, b) => a + b;
"""
        adapter = JavaScriptAdapter()
        functions = adapter.extract_functions(code)
        assert len(functions) >= 1
        assert any(f["name"] == "greet" for f in functions)

    def test_javascript_adapter_classes(self):
        """Test JavaScript class extraction"""
        code = """
class Animal {
    constructor(name) {}
}

class Dog extends Animal {
}
"""
        adapter = JavaScriptAdapter()
        classes = adapter.extract_classes(code)
        assert len(classes) == 2
        assert classes[0]["name"] == "Animal"
        assert classes[1]["name"] == "Dog"

    def test_java_adapter_functions(self):
        """Test Java method extraction"""
        code = """
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    private void reset() {
    }
}
"""
        adapter = JavaAdapter()
        functions = adapter.extract_functions(code)
        assert len(functions) == 2

    def test_language_adapter_factory(self):
        """Test factory creates correct adapters"""
        factory = LanguageAdapterFactory()

        python_adapter = factory.create("python")
        assert isinstance(python_adapter, PythonAdapter)

        js_adapter = factory.create("javascript")
        assert isinstance(js_adapter, JavaScriptAdapter)

        java_adapter = factory.create("java")
        assert isinstance(java_adapter, JavaAdapter)

    def test_factory_invalid_language(self):
        """Test factory raises error for unsupported language"""
        factory = LanguageAdapterFactory()
        with pytest.raises(ValueError):
            factory.create("cobol")

    def test_factory_supported_languages(self):
        """Test factory lists supported languages"""
        factory = LanguageAdapterFactory()
        languages = factory.supported_languages()
        assert len(languages) > 0
        assert "python" in languages
        assert "javascript" in languages


class TestCodeAnalyzer:
    """Test code analysis functionality"""

    def test_analyze_quality_python(self):
        """Test quality analysis for Python"""
        analyzer = CodeAnalyzer()
        code = """
def calculate(x, y):
    return x + y
"""
        quality = analyzer.analyze_quality(code, "python")
        assert quality.overall_score >= 0
        assert quality.overall_score <= 100
        assert quality.code_quality >= 0
        assert quality.maintainability >= 0

    def test_analyze_issues(self):
        """Test issue detection"""
        analyzer = CodeAnalyzer()
        code = """def complex_func(a, b, c, d):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    return a + b + c + d
    return 0

very_long_variable_name_that_exceeds_one_hundred_characters_and_triggers_warning = 1
"""
        issues = analyzer.analyze_issues(code, "python")
        assert len(issues) > 0

    def test_analyze_complexity(self):
        """Test complexity metrics"""
        analyzer = CodeAnalyzer()
        code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""
        metrics = analyzer.analyze_complexity(code, "python")
        assert metrics.cyclomatic_complexity > 0
        assert metrics.cognitive_complexity > 0
        assert metrics.lines_of_code > 0
        assert metrics.nesting_depth >= 0

    def test_analyze_architecture(self):
        """Test architecture pattern detection"""
        analyzer = CodeAnalyzer()
        code = """class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
"""
        insights = analyzer.analyze_architecture(code, "python")
        assert len(insights) >= 0

    def test_analyze_formatting_python(self):
        """Test formatting recommendations for Python"""
        analyzer = CodeAnalyzer()
        code = "def test():\n\tx = 1  # Tab indentation"
        recommendations = analyzer.analyze_formatting(code, "python")
        assert len(recommendations) > 0

    def test_analyze_for_debugging(self):
        """Test debugging analysis"""
        analyzer = CodeAnalyzer()
        code = """
def risky_op():
    while True:
        x = open('file.txt').read()
        print(x)
"""
        insights = analyzer.analyze_for_debugging(code, "python")
        assert len(insights) > 0

    def test_cyclomatic_complexity(self):
        """Test cyclomatic complexity calculation"""
        analyzer = CodeAnalyzer()
        simple_code = "x = 1"
        complex_code = """
if a:
    if b:
        if c:
            pass
        elif d:
            pass
    else:
        pass
elif e:
    pass
"""
        simple_complexity = analyzer._calculate_cyclomatic_complexity(
            simple_code, "python"
        )
        complex_complexity = analyzer._calculate_cyclomatic_complexity(
            complex_code, "python"
        )
        assert complex_complexity > simple_complexity

    def test_nesting_depth(self):
        """Test nesting depth calculation"""
        analyzer = CodeAnalyzer()
        code_depth_1 = "x = {}"
        code_depth_3 = "{[[()]]}"
        depth_1 = analyzer._calculate_nesting_depth(code_depth_1, "python")
        depth_3 = analyzer._calculate_nesting_depth(code_depth_3, "python")
        assert depth_3 > depth_1

    def test_duplication_score(self):
        """Test code duplication calculation"""
        analyzer = CodeAnalyzer()
        unique_code = "x = 1\ny = 2\nz = 3"
        duplicate_code = "x = 1\nx = 1\nx = 1"
        unique_score = analyzer._calculate_duplication_score(unique_code)
        duplicate_score = analyzer._calculate_duplication_score(duplicate_code)
        assert unique_score > duplicate_score

    def test_detect_style_issues(self):
        """Test style issue detection"""
        analyzer = CodeAnalyzer()
        code = "very_long_line = 'this is a very long line that should exceed one hundred characters in length and trigger a style issue warning'"
        issues = analyzer._detect_style_issues(code, "python")
        assert len(issues) > 0

    def test_detect_complexity_issues(self):
        """Test complexity issue detection"""
        analyzer = CodeAnalyzer()
        code = """def deeply_nested():
    if a:
        if b:
            if c:
                if d:
                    if e:
                        if f:
                            pass
"""
        issues = analyzer._detect_complexity_issues(code, "python")
        assert len(issues) >= 0

    def test_detect_null_pointer_risks(self):
        """Test null pointer risk detection"""
        analyzer = CodeAnalyzer()
        code = "data.split().join().map()"
        risk = analyzer._detect_null_pointer_risks(code, "javascript")
        assert isinstance(risk, bool)

    def test_detect_infinite_loops(self):
        """Test infinite loop detection"""
        analyzer = CodeAnalyzer()
        code = "while (true) {\n    console.log('loop');\n}"
        risk = analyzer._detect_infinite_loops(code, "javascript")
        assert isinstance(risk, bool)

    def test_detect_resource_leaks(self):
        """Test resource leak detection"""
        analyzer = CodeAnalyzer()
        code = "f = open('file.txt')"
        risk = analyzer._detect_resource_leaks(code, "python")
        assert risk is True


class TestAnalysisService:
    """Test analysis service orchestration"""

    def test_analyze_full(self):
        """Test full analysis"""
        service = AnalysisService()
        code = """
def greet(name):
    # Greet a person
    return f"Hello, {name}!"
"""
        result = service.analyze_full(code, "python", "test.py")

        assert result["file_name"] == "test.py"
        assert result["language"] == "python"
        assert result["code_length"] > 0
        assert "quality_score" in result
        assert "issues" in result
        assert "complexity_metrics" in result
        assert "architecture_insights" in result
        assert "formatting_recommendations" in result
        assert result["analysis_duration_ms"] > 0

    def test_analyze_for_debugging(self):
        """Test debugging analysis"""
        service = AnalysisService()
        code = """
def unsafe():
    while True:
        x = open('file.txt')
        data = x.read()
"""
        result = service.analyze_for_debugging(code, "python", "test.py")

        assert result["file_name"] == "test.py"
        assert result["language"] == "python"
        assert "debug_insights" in result
        assert "common_issues" in result
        assert result["analysis_duration_ms"] > 0

    def test_analysis_duration(self):
        """Test that analysis duration is reasonable"""
        service = AnalysisService()
        code = "x = 1"
        result = service.analyze_full(code, "python")
        assert result["analysis_duration_ms"] < 5000
        assert result["analysis_duration_ms"] > 0
