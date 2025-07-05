"""Performance benchmarking for audiobook organization."""

from __future__ import annotations

import time
from typing import Dict, List, Any
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class OperationStats:
    """Statistics for a single operation."""
    name: str
    start_time: float
    end_time: float = 0.0
    success: bool = True
    error_message: str = ""
    
    @property
    def duration(self) -> float:
        """Get operation duration in seconds."""
        return self.end_time - self.start_time if self.end_time > 0 else 0.0


@dataclass
class AudiobookStats:
    """Statistics for processing a single audiobook."""
    folder_name: str
    total_time: float = 0.0
    metadata_extraction_time: float = 0.0
    api_fetch_time: float = 0.0
    genre_inference_time: float = 0.0
    tag_update_time: float = 0.0
    file_move_time: float = 0.0
    file_count: int = 0
    operations: List[OperationStats] = field(default_factory=list)
    
    def add_operation(self, operation: OperationStats):
        """Add an operation to this audiobook's stats."""
        self.operations.append(operation)


class BenchmarkCollector:
    """Collects and manages benchmark data."""
    
    def __init__(self):
        """Initialize the benchmark collector."""
        self.overall_start_time = time.time()
        self.overall_end_time = 0.0
        self.audiobook_stats: Dict[str, AudiobookStats] = {}
        self.current_operations: Dict[str, OperationStats] = {}
    
    def start_operation(self, operation_name: str, context: str = "") -> str:
        """Start timing an operation.
        
        Parameters
        ----------
        operation_name: str
            Name of the operation
        context: str
            Additional context (e.g., folder name)
            
        Returns
        -------
        str
            Operation ID for later reference
        """
        op_id = f"{operation_name}_{context}_{time.time()}"
        operation = OperationStats(
            name=operation_name,
            start_time=time.time()
        )
        self.current_operations[op_id] = operation
        return op_id
    
    def end_operation(self, op_id: str, success: bool = True, error_message: str = ""):
        """End timing an operation.
        
        Parameters
        ----------
        op_id: str
            Operation ID returned by start_operation
        success: bool
            Whether the operation succeeded
        error_message: str
            Error message if operation failed
        """
        if op_id in self.current_operations:
            operation = self.current_operations[op_id]
            operation.end_time = time.time()
            operation.success = success
            operation.error_message = error_message
            del self.current_operations[op_id]
    
    def add_audiobook_stat(self, folder_name: str, stats: AudiobookStats):
        """Add statistics for an audiobook."""
        self.audiobook_stats[folder_name] = stats
    
    def finish_benchmark(self):
        """Mark the end of benchmarking."""
        self.overall_end_time = time.time()
    
    @property
    def total_duration(self) -> float:
        """Get total benchmark duration."""
        end_time = self.overall_end_time if self.overall_end_time > 0 else time.time()
        return end_time - self.overall_start_time
    
    def get_summary(self) -> Dict[str, Any]:
        """Get benchmark summary statistics."""
        if not self.audiobook_stats:
            return {"total_duration": self.total_duration, "audiobooks_processed": 0}
        
        total_books = len(self.audiobook_stats)
        total_processing_time = sum(stats.total_time for stats in self.audiobook_stats.values())
        avg_time_per_book = total_processing_time / total_books if total_books > 0 else 0
        
        # Find fastest and slowest books
        fastest_book = min(self.audiobook_stats.values(), key=lambda s: s.total_time)
        slowest_book = max(self.audiobook_stats.values(), key=lambda s: s.total_time)
        
        # Calculate operation breakdowns
        operation_times = {
            "metadata_extraction": sum(s.metadata_extraction_time for s in self.audiobook_stats.values()),
            "api_fetch": sum(s.api_fetch_time for s in self.audiobook_stats.values()),
            "genre_inference": sum(s.genre_inference_time for s in self.audiobook_stats.values()),
            "tag_update": sum(s.tag_update_time for s in self.audiobook_stats.values()),
            "file_move": sum(s.file_move_time for s in self.audiobook_stats.values()),
        }
        
        return {
            "total_duration": self.total_duration,
            "audiobooks_processed": total_books,
            "total_processing_time": total_processing_time,
            "avg_time_per_book": avg_time_per_book,
            "fastest_book": {
                "name": fastest_book.folder_name,
                "time": fastest_book.total_time
            },
            "slowest_book": {
                "name": slowest_book.folder_name,
                "time": slowest_book.total_time
            },
            "operation_breakdown": operation_times,
            "throughput_books_per_second": total_books / self.total_duration if self.total_duration > 0 else 0
        }
    
    def print_summary(self):
        """Print benchmark summary to console."""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("📊 PERFORMANCE BENCHMARK SUMMARY")
        print("="*60)
        
        print(f"Total Duration: {summary['total_duration']:.2f}s")
        print(f"Audiobooks Processed: {summary['audiobooks_processed']}")
        print(f"Average Time per Book: {summary['avg_time_per_book']:.2f}s")
        print(f"Throughput: {summary['throughput_books_per_second']:.2f} books/sec")
        
        if summary['audiobooks_processed'] > 0:
            print(f"\nFastest Book: {summary['fastest_book']['name']} ({summary['fastest_book']['time']:.2f}s)")
            print(f"Slowest Book: {summary['slowest_book']['name']} ({summary['slowest_book']['time']:.2f}s)")
            
            print("\nOperation Breakdown:")
            for operation, duration in summary['operation_breakdown'].items():
                percentage = (duration / summary['total_processing_time']) * 100 if summary['total_processing_time'] > 0 else 0
                print(f"  {operation.replace('_', ' ').title()}: {duration:.2f}s ({percentage:.1f}%)")
        
        print("="*60)
    
    def print_detailed_report(self):
        """Print detailed per-book benchmark report."""
        if not self.audiobook_stats:
            print("No benchmark data available.")
            return
        
        print("\n" + "="*80)
        print("📈 DETAILED PERFORMANCE REPORT")
        print("="*80)
        
        # Sort by total time
        sorted_stats = sorted(self.audiobook_stats.values(), key=lambda s: s.total_time, reverse=True)
        
        print(f"{'Book Name':<30} {'Total':<8} {'Metadata':<10} {'API':<8} {'Genre':<8} {'Tags':<8} {'Move':<8} {'Files':<6}")
        print("-" * 80)
        
        for stats in sorted_stats:
            print(f"{stats.folder_name[:29]:<30} "
                  f"{stats.total_time:<8.2f} "
                  f"{stats.metadata_extraction_time:<10.2f} "
                  f"{stats.api_fetch_time:<8.2f} "
                  f"{stats.genre_inference_time:<8.2f} "
                  f"{stats.tag_update_time:<8.2f} "
                  f"{stats.file_move_time:<8.2f} "
                  f"{stats.file_count:<6}")
        
        print("="*80)


# Global benchmark collector
_benchmark_collector: BenchmarkCollector = BenchmarkCollector()


def get_benchmark_collector() -> BenchmarkCollector:
    """Get the global benchmark collector."""
    return _benchmark_collector


def reset_benchmark_collector():
    """Reset the global benchmark collector."""
    global _benchmark_collector
    _benchmark_collector = BenchmarkCollector()


class TimedOperation:
    """Context manager for timing operations."""
    
    def __init__(self, operation_name: str, context: str = "", collector: BenchmarkCollector = None):
        """Initialize timed operation.
        
        Parameters
        ----------
        operation_name: str
            Name of the operation
        context: str
            Additional context
        collector: BenchmarkCollector
            Collector to use, defaults to global collector
        """
        self.operation_name = operation_name
        self.context = context
        self.collector = collector or get_benchmark_collector()
        self.op_id: str = ""
    
    def __enter__(self):
        """Start timing the operation."""
        self.op_id = self.collector.start_operation(self.operation_name, self.context)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End timing the operation."""
        success = exc_type is None
        error_message = str(exc_val) if exc_val else ""
        self.collector.end_operation(self.op_id, success, error_message)