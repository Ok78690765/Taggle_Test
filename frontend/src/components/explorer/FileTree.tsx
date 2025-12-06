'use client';

import React, { useState } from 'react';
import clsx from 'clsx';
import type { FileNode } from '@/types';

interface FileTreeProps {
  nodes: FileNode[];
  selectedPath: string | null;
  onSelect: (node: FileNode) => void;
}

export function FileTree({ nodes, selectedPath, onSelect }: FileTreeProps) {
  return (
    <div className="space-y-1">
      {nodes.map((node) => (
        <TreeNode
          key={node.path}
          node={node}
          level={0}
          selectedPath={selectedPath}
          onSelect={onSelect}
        />
      ))}
    </div>
  );
}

interface TreeNodeProps {
  node: FileNode;
  level: number;
  selectedPath: string | null;
  onSelect: (node: FileNode) => void;
}

function TreeNode({ node, level, selectedPath, onSelect }: TreeNodeProps) {
  const [expanded, setExpanded] = useState(level < 1);
  const isDirectory = node.type === 'directory';
  const isSelected = selectedPath === node.path;

  const handleClick = () => {
    if (isDirectory) {
      setExpanded((prev) => !prev);
    } else {
      onSelect(node);
    }
  };

  return (
    <div>
      <button
        type="button"
        className={clsx(
          'flex w-full items-center gap-2 rounded-lg px-3 py-1.5 text-left text-sm transition',
          isSelected ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-50'
        )}
        style={{ paddingLeft: `${level * 16 + 12}px` }}
        onClick={handleClick}
      >
        {isDirectory ? (
          <svg
            className="h-4 w-4 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            {expanded ? (
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            ) : (
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            )}
          </svg>
        ) : (
          <span className="h-1.5 w-1.5 rounded-full bg-gray-400" />
        )}
        <span className="font-medium">
          {node.name}
          {isDirectory && (
            <span className="ml-2 text-xs text-gray-400">
              {node.children?.length ?? 0}
            </span>
          )}
        </span>
      </button>
      {isDirectory && expanded && node.children && (
        <div className="mt-1 space-y-1">
          {node.children.map((child) => (
            <TreeNode
              key={child.path}
              node={child}
              level={level + 1}
              selectedPath={selectedPath}
              onSelect={onSelect}
            />
          ))}
        </div>
      )}
    </div>
  );
}
