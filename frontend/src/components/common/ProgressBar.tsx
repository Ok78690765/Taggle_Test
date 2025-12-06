import React from 'react';
import clsx from 'clsx';

interface ProgressBarProps {
  value: number;
  max?: number;
  label?: string;
  showPercentage?: boolean;
  color?: 'blue' | 'green' | 'amber' | 'red';
  size?: 'sm' | 'md' | 'lg';
}

export function ProgressBar({
  value,
  max = 100,
  label,
  showPercentage = false,
  color = 'blue',
  size = 'md',
}: ProgressBarProps) {
  const percentage = Math.min((value / max) * 100, 100);

  const colors = {
    blue: 'bg-blue-600',
    green: 'bg-green-600',
    amber: 'bg-amber-600',
    red: 'bg-red-600',
  };

  const sizes = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3',
  };

  return (
    <div className="w-full">
      {(label || showPercentage) && (
        <div className="flex items-center justify-between mb-1">
          {label && <span className="text-sm font-medium text-gray-700">{label}</span>}
          {showPercentage && (
            <span className="text-sm font-medium text-gray-600">
              {Math.round(percentage)}%
            </span>
          )}
        </div>
      )}
      <div className={clsx('w-full bg-gray-200 rounded-full overflow-hidden', sizes[size])}>
        <div
          className={clsx('h-full transition-all duration-300 ease-out', colors[color])}
          style={{ width: `${percentage}%` }}
          role="progressbar"
          aria-valuenow={value}
          aria-valuemin={0}
          aria-valuemax={max}
        />
      </div>
    </div>
  );
}
