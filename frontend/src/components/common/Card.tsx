import React from 'react';
import clsx from 'clsx';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  padding?: 'sm' | 'md' | 'lg' | 'none';
  shadow?: boolean;
  title?: string;
  subtitle?: string;
  actions?: React.ReactNode;
}

export function Card({
  children,
  padding = 'md',
  shadow = true,
  title,
  subtitle,
  actions,
  className,
  ...props
}: CardProps) {
  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  return (
    <section
      className={clsx(
        'rounded-2xl border border-gray-100 bg-white',
        shadow && 'shadow-sm',
        paddingClasses[padding],
        className
      )}
      {...props}
    >
      {(title || actions) && (
        <header className="mb-4 flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
          <div>
            {title && (
              <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
            )}
            {subtitle && (
              <p className="text-sm text-gray-500">{subtitle}</p>
            )}
          </div>
          {actions && <div className="flex items-center gap-2">{actions}</div>}
        </header>
      )}
      {children}
    </section>
  );
}
