import React from 'react';
import clsx from 'clsx';

interface StatusPillProps {
  label: string;
  status?: 'success' | 'warning' | 'error' | 'info' | 'neutral';
}

export function StatusPill({ label, status = 'neutral' }: StatusPillProps) {
  const styles = {
    success: 'bg-green-50 text-green-700 border-green-200',
    warning: 'bg-amber-50 text-amber-700 border-amber-200',
    error: 'bg-red-50 text-red-700 border-red-200',
    info: 'bg-blue-50 text-blue-700 border-blue-200',
    neutral: 'bg-gray-50 text-gray-600 border-gray-200',
  };

  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wide',
        styles[status]
      )}
    >
      {label}
    </span>
  );
}
