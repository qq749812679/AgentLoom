from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

import numpy as np

from ..core.logger import JsonlLogger
from ..core.cache import SimpleDiskCache


@dataclass
class PerformanceMetrics:
    latency_ms: float
    throughput_rps: float
    error_rate: float
    memory_usage_mb: float
    gpu_utilization: float
    quality_score: float


@dataclass
class OptimizationStrategy:
    name: str
    description: str
    parameters: Dict[str, Any]
    expected_improvement: float


class ModelOptimizer:
    def __init__(self, logger: JsonlLogger, cache: SimpleDiskCache) -> None:
        self.logger = logger
        self.cache = cache
        self.performance_history: List[PerformanceMetrics] = []
        self.optimization_strategies: List[OptimizationStrategy] = []
        self._initialize_strategies()
    
    def _initialize_strategies(self) -> None:
        """Initialize available optimization strategies"""
        self.optimization_strategies = [
            OptimizationStrategy(
                name="dynamic_batching",
                description="动态批处理优化，根据负载自动调整批大小",
                parameters={"min_batch_size": 1, "max_batch_size": 8, "timeout_ms": 100},
                expected_improvement=0.3
            ),
            OptimizationStrategy(
                name="model_quantization",
                description="模型量化，减少内存使用和推理时间",
                parameters={"precision": "int8", "calibration_samples": 100},
                expected_improvement=0.4
            ),
            OptimizationStrategy(
                name="cache_optimization",
                description="智能缓存策略，减少重复计算",
                parameters={"cache_size": 1000, "ttl_hours": 24, "similarity_threshold": 0.9},
                expected_improvement=0.6
            ),
            OptimizationStrategy(
                name="prompt_optimization",
                description="提示词优化，提高生成质量和效率",
                parameters={"length_limit": 500, "template_optimization": True},
                expected_improvement=0.2
            ),
            OptimizationStrategy(
                name="adaptive_resolution",
                description="自适应分辨率，根据内容复杂度调整",
                parameters={"min_resolution": 512, "max_resolution": 1024, "complexity_threshold": 0.7},
                expected_improvement=0.25
            )
        ]
    
    def measure_performance(self, model_func: Callable, inputs: List[Any], model_name: str) -> PerformanceMetrics:
        """Measure model performance metrics"""
        start_time = time.time()
        errors = 0
        results = []
        
        # Simulate memory and GPU monitoring
        initial_memory = self._get_memory_usage()
        
        for input_data in inputs:
            try:
                result = model_func(input_data)
                results.append(result)
            except Exception as e:
                errors += 1
                self.logger.log({"event": "model.performance.error", "model": model_name, "error": str(e)})
        
        end_time = time.time()
        total_time_ms = (end_time - start_time) * 1000
        
        metrics = PerformanceMetrics(
            latency_ms=total_time_ms / len(inputs) if inputs else 0,
            throughput_rps=len(inputs) / (total_time_ms / 1000) if total_time_ms > 0 else 0,
            error_rate=errors / len(inputs) if inputs else 0,
            memory_usage_mb=self._get_memory_usage() - initial_memory,
            gpu_utilization=self._get_gpu_utilization(),
            quality_score=self._calculate_quality_score(results)
        )
        
        self.performance_history.append(metrics)
        self.logger.log({
            "event": "model.performance.measured",
            "model": model_name,
            "metrics": {
                "latency_ms": metrics.latency_ms,
                "throughput_rps": metrics.throughput_rps,
                "error_rate": metrics.error_rate,
                "quality_score": metrics.quality_score
            }
        })
        
        return metrics
    
    def suggest_optimizations(self, current_metrics: PerformanceMetrics, target_metrics: Dict[str, float]) -> List[OptimizationStrategy]:
        """Suggest optimization strategies based on current performance"""
        suggestions = []
        
        # Analyze performance gaps
        if current_metrics.latency_ms > target_metrics.get("latency_ms", 1000):
            suggestions.extend([
                s for s in self.optimization_strategies 
                if s.name in ["dynamic_batching", "model_quantization", "cache_optimization"]
            ])
        
        if current_metrics.memory_usage_mb > target_metrics.get("memory_usage_mb", 2000):
            suggestions.extend([
                s for s in self.optimization_strategies 
                if s.name in ["model_quantization", "adaptive_resolution"]
            ])
        
        if current_metrics.quality_score < target_metrics.get("quality_score", 0.8):
            suggestions.extend([
                s for s in self.optimization_strategies 
                if s.name in ["prompt_optimization"]
            ])
        
        if current_metrics.throughput_rps < target_metrics.get("throughput_rps", 1.0):
            suggestions.extend([
                s for s in self.optimization_strategies 
                if s.name in ["dynamic_batching", "cache_optimization"]
            ])
        
        # Remove duplicates and sort by expected improvement
        unique_suggestions = {s.name: s for s in suggestions}.values()
        return sorted(unique_suggestions, key=lambda s: s.expected_improvement, reverse=True)
    
    def apply_optimization(self, strategy: OptimizationStrategy, model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply optimization strategy to model configuration"""
        optimized_config = model_config.copy()
        
        if strategy.name == "dynamic_batching":
            optimized_config.update({
                "batch_size": "dynamic",
                "min_batch_size": strategy.parameters["min_batch_size"],
                "max_batch_size": strategy.parameters["max_batch_size"],
                "batch_timeout_ms": strategy.parameters["timeout_ms"]
            })
        
        elif strategy.name == "model_quantization":
            optimized_config.update({
                "precision": strategy.parameters["precision"],
                "quantization_enabled": True,
                "calibration_samples": strategy.parameters["calibration_samples"]
            })
        
        elif strategy.name == "cache_optimization":
            optimized_config.update({
                "caching_enabled": True,
                "cache_size": strategy.parameters["cache_size"],
                "cache_ttl_hours": strategy.parameters["ttl_hours"],
                "similarity_threshold": strategy.parameters["similarity_threshold"]
            })
        
        elif strategy.name == "prompt_optimization":
            optimized_config.update({
                "prompt_length_limit": strategy.parameters["length_limit"],
                "template_optimization": strategy.parameters["template_optimization"],
                "prompt_preprocessing": True
            })
        
        elif strategy.name == "adaptive_resolution":
            optimized_config.update({
                "adaptive_resolution": True,
                "min_resolution": strategy.parameters["min_resolution"],
                "max_resolution": strategy.parameters["max_resolution"],
                "complexity_threshold": strategy.parameters["complexity_threshold"]
            })
        
        self.logger.log({
            "event": "optimization.applied",
            "strategy": strategy.name,
            "parameters": strategy.parameters
        })
        
        return optimized_config
    
    def auto_tune(self, model_func: Callable, test_inputs: List[Any], target_metrics: Dict[str, float], model_name: str) -> Dict[str, Any]:
        """Automatically tune model for optimal performance"""
        self.logger.log({"event": "auto_tune.start", "model": model_name})
        
        # Baseline measurement
        baseline_metrics = self.measure_performance(model_func, test_inputs, model_name)
        best_config = {}
        best_metrics = baseline_metrics
        
        # Get optimization suggestions
        suggestions = self.suggest_optimizations(baseline_metrics, target_metrics)
        
        tuning_results = {
            "baseline_metrics": baseline_metrics,
            "optimizations_tested": [],
            "best_config": best_config,
            "best_metrics": best_metrics,
            "improvement_percentage": 0.0
        }
        
        # Test each optimization
        for strategy in suggestions[:3]:  # Test top 3 suggestions
            test_config = self.apply_optimization(strategy, {})
            
            # Simulate testing optimized configuration
            # In real implementation, this would reconfigure and test the model
            simulated_metrics = self._simulate_optimized_performance(baseline_metrics, strategy)
            
            optimization_result = {
                "strategy": strategy.name,
                "config": test_config,
                "metrics": simulated_metrics,
                "improvement": self._calculate_improvement(baseline_metrics, simulated_metrics)
            }
            
            tuning_results["optimizations_tested"].append(optimization_result)
            
            # Update best configuration if this is better
            if self._is_better_metrics(simulated_metrics, best_metrics, target_metrics):
                best_config = test_config
                best_metrics = simulated_metrics
        
        # Calculate overall improvement
        tuning_results["best_config"] = best_config
        tuning_results["best_metrics"] = best_metrics
        tuning_results["improvement_percentage"] = self._calculate_improvement(baseline_metrics, best_metrics)
        
        self.logger.log({
            "event": "auto_tune.complete",
            "model": model_name,
            "improvement": tuning_results["improvement_percentage"],
            "optimizations_applied": len(tuning_results["optimizations_tested"])
        })
        
        return tuning_results
    
    def _simulate_optimized_performance(self, baseline: PerformanceMetrics, strategy: OptimizationStrategy) -> PerformanceMetrics:
        """Simulate performance after applying optimization"""
        improvement_factor = strategy.expected_improvement
        
        return PerformanceMetrics(
            latency_ms=baseline.latency_ms * (1 - improvement_factor * 0.5),
            throughput_rps=baseline.throughput_rps * (1 + improvement_factor),
            error_rate=baseline.error_rate * (1 - improvement_factor * 0.3),
            memory_usage_mb=baseline.memory_usage_mb * (1 - improvement_factor * 0.4),
            gpu_utilization=baseline.gpu_utilization * (1 + improvement_factor * 0.2),
            quality_score=min(1.0, baseline.quality_score * (1 + improvement_factor * 0.1))
        )
    
    def _calculate_improvement(self, baseline: PerformanceMetrics, optimized: PerformanceMetrics) -> float:
        """Calculate overall improvement percentage"""
        latency_improvement = (baseline.latency_ms - optimized.latency_ms) / baseline.latency_ms
        throughput_improvement = (optimized.throughput_rps - baseline.throughput_rps) / baseline.throughput_rps if baseline.throughput_rps > 0 else 0
        quality_improvement = (optimized.quality_score - baseline.quality_score) / baseline.quality_score if baseline.quality_score > 0 else 0
        
        return (latency_improvement + throughput_improvement + quality_improvement) / 3 * 100
    
    def _is_better_metrics(self, metrics1: PerformanceMetrics, metrics2: PerformanceMetrics, targets: Dict[str, float]) -> bool:
        """Compare two metrics sets considering target preferences"""
        score1 = self._calculate_metrics_score(metrics1, targets)
        score2 = self._calculate_metrics_score(metrics2, targets)
        return score1 > score2
    
    def _calculate_metrics_score(self, metrics: PerformanceMetrics, targets: Dict[str, float]) -> float:
        """Calculate overall score for metrics"""
        weights = {"latency": 0.3, "throughput": 0.2, "quality": 0.3, "memory": 0.2}
        
        latency_score = 1 - min(1, metrics.latency_ms / targets.get("latency_ms", 1000))
        throughput_score = min(1, metrics.throughput_rps / targets.get("throughput_rps", 1))
        quality_score = metrics.quality_score
        memory_score = 1 - min(1, metrics.memory_usage_mb / targets.get("memory_usage_mb", 2000))
        
        return (
            weights["latency"] * latency_score +
            weights["throughput"] * throughput_score +
            weights["quality"] * quality_score +
            weights["memory"] * memory_score
        )
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB (mock implementation)"""
        # In real implementation, would use psutil or similar
        return np.random.uniform(500, 1500)
    
    def _get_gpu_utilization(self) -> float:
        """Get current GPU utilization (mock implementation)"""
        # In real implementation, would use nvidia-ml-py or similar
        return np.random.uniform(0.3, 0.9)
    
    def _calculate_quality_score(self, results: List[Any]) -> float:
        """Calculate quality score for generated results"""
        # Mock quality calculation - in real implementation would use actual quality metrics
        if not results:
            return 0.0
        return np.random.uniform(0.7, 0.95)
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        if not self.performance_history:
            return {"error": "No performance data available"}
        
        recent_metrics = self.performance_history[-10:]  # Last 10 measurements
        
        report = {
            "summary": {
                "total_measurements": len(self.performance_history),
                "avg_latency_ms": np.mean([m.latency_ms for m in recent_metrics]),
                "avg_throughput_rps": np.mean([m.throughput_rps for m in recent_metrics]),
                "avg_quality_score": np.mean([m.quality_score for m in recent_metrics]),
                "error_rate": np.mean([m.error_rate for m in recent_metrics])
            },
            "trends": {
                "latency_trend": "stable" if len(recent_metrics) < 3 else self._calculate_trend([m.latency_ms for m in recent_metrics[-3:]]),
                "quality_trend": "stable" if len(recent_metrics) < 3 else self._calculate_trend([m.quality_score for m in recent_metrics[-3:]]),
            },
            "recommendations": self._generate_performance_recommendations(recent_metrics)
        }
        
        return report
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction for a list of values"""
        if len(values) < 2:
            return "stable"
        
        trend = np.polyfit(range(len(values)), values, 1)[0]
        if abs(trend) < 0.01:
            return "stable"
        elif trend > 0:
            return "improving"
        else:
            return "declining"
    
    def _generate_performance_recommendations(self, recent_metrics: List[PerformanceMetrics]) -> List[str]:
        """Generate performance improvement recommendations"""
        recommendations = []
        
        if not recent_metrics:
            return recommendations
        
        avg_latency = np.mean([m.latency_ms for m in recent_metrics])
        avg_quality = np.mean([m.quality_score for m in recent_metrics])
        avg_error_rate = np.mean([m.error_rate for m in recent_metrics])
        
        if avg_latency > 2000:
            recommendations.append("延迟过高，建议启用批处理优化或模型量化")
        
        if avg_quality < 0.8:
            recommendations.append("质量分数偏低，建议优化提示词或调整模型参数")
        
        if avg_error_rate > 0.05:
            recommendations.append("错误率偏高，建议检查输入验证和异常处理")
        
        if len(recommendations) == 0:
            recommendations.append("性能表现良好，可考虑进一步优化以提升用户体验")
        
        return recommendations
