import React from 'react';
import { Button } from './Button';

interface EmptyStateProps {
  title: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
}

export function EmptyState({
  title,
  description,
  actionLabel,
  onAction,
}: EmptyStateProps) {
  return (
    <div className="rounded-2xl border border-dashed border-gray-200 bg-gray-50 p-8 text-center">
      <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
      {description && <p className="mt-2 text-sm text-gray-500">{description}</p>}
      {actionLabel && (
        <Button
          variant="outline"
          size="sm"
          className="mt-4"
          onClick={onAction}
        >
          {actionLabel}
        </Button>
      )}
    </div>
  );
}
