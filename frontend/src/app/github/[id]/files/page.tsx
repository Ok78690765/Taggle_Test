'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { RepositoryService, FileTreeNode, CodeInspectionResponse } from '@/lib/repository-service';

export default function RepositoryFilesPage() {
  const params = useParams();
  const router = useRouter();
  const repoId = parseInt(params.id as string, 10);

  const [fileTree, setFileTree] = useState<FileTreeNode | null>(null);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState<CodeInspectionResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [contentLoading, setContentLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedDirs, setExpandedDirs] = useState<Set<string>>(new Set());

  useEffect(() => {
    const loadFileTree = async () => {
      try {
        setLoading(true);
        const tree = await RepositoryService.getFileTree(repoId);
        setFileTree(tree.root);
        setError(null);
      } catch (err) {
        setError('Failed to load file tree');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadFileTree();
  }, [repoId]);

  const handleFileSelect = async (path: string, type: string) => {
    if (type === 'directory') {
      const newExpanded = new Set(expandedDirs);
      if (newExpanded.has(path)) {
        newExpanded.delete(path);
      } else {
        newExpanded.add(path);
      }
      setExpandedDirs(newExpanded);
      return;
    }

    try {
      setSelectedFile(path);
      setContentLoading(true);
      const content = await RepositoryService.inspectCodeFile(repoId, path);
      setFileContent(content);
    } catch (err) {
      setError('Failed to load file content');
      console.error(err);
    } finally {
      setContentLoading(false);
    }
  };

  const renderFileTree = (node: FileTreeNode, level: number = 0): JSX.Element => {
    const isExpanded = expandedDirs.has(node.path);

    if (node.type === 'directory') {
      return (
        <div key={node.path}>
          <div
            onClick={() => handleFileSelect(node.path, 'directory')}
            className="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer rounded"
            style={{ paddingLeft: `${level * 20 + 8}px` }}
          >
            <span className="text-xs">{isExpanded ? '▼' : '▶'}</span>
            <span className="text-gray-700">📁 {node.path.split('/').pop()}</span>
          </div>
          {isExpanded &&
            node.children?.map((child) => renderFileTree(child, level + 1))}
        </div>
      );
    }

    return (
      <div
        key={node.path}
        onClick={() => handleFileSelect(node.path, 'file')}
        className={`flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer rounded ${
          selectedFile === node.path ? 'bg-blue-50' : ''
        }`}
        style={{ paddingLeft: `${level * 20 + 8}px` }}
      >
        <span className="text-gray-700">📄 {node.path.split('/').pop()}</span>
        {node.size && (
          <span className="text-xs text-gray-500">
            ({(node.size / 1024).toFixed(1)}KB)
          </span>
        )}
      </div>
    );
  };

  const getLanguageFromPath = (path: string): string | undefined => {
    const ext = path.split('.').pop()?.toLowerCase();
    const languageMap: { [key: string]: string } = {
      py: 'python',
      js: 'javascript',
      ts: 'typescript',
      jsx: 'jsx',
      tsx: 'tsx',
      go: 'go',
      rs: 'rust',
      java: 'java',
      cpp: 'cpp',
      c: 'c',
      cs: 'csharp',
      rb: 'ruby',
      php: 'php',
      swift: 'swift',
      kt: 'kotlin',
      scala: 'scala',
      html: 'html',
      css: 'css',
      scss: 'scss',
      json: 'json',
      xml: 'xml',
      yaml: 'yaml',
      yml: 'yaml',
      md: 'markdown',
      sql: 'sql',
    };
    return languageMap[ext || ''];
  };

  return (
    <main className="container mx-auto py-12">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6 flex items-center">
          <button
            onClick={() => router.back()}
            className="text-blue-600 hover:text-blue-800 mr-4"
          >
            ← Back
          </button>
          <h1 className="text-3xl font-bold">Repository Files</h1>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-lg border border-red-200">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <div className="px-4 py-3 bg-gray-50 border-b">
                <h2 className="font-semibold text-gray-900">Files</h2>
              </div>
              <div className="max-h-96 overflow-y-auto">
                {loading ? (
                  <div className="p-4 text-center text-gray-500">
                    Loading files...
                  </div>
                ) : fileTree ? (
                  renderFileTree(fileTree)
                ) : (
                  <div className="p-4 text-center text-gray-500">
                    No files found
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow overflow-hidden">
              {selectedFile ? (
                <div className="flex flex-col h-full">
                  <div className="px-4 py-3 bg-gray-50 border-b">
                    <h2 className="font-semibold text-gray-900 break-all">
                      {selectedFile}
                    </h2>
                  </div>
                  <div className="flex-1 overflow-auto">
                    {contentLoading ? (
                      <div className="p-4 text-center text-gray-500">
                        Loading file content...
                      </div>
                    ) : fileContent ? (
                      <div className="p-4">
                        <pre className="bg-gray-900 text-gray-100 p-4 rounded overflow-x-auto text-sm font-mono max-h-96">
                          <code>{fileContent.content}</code>
                        </pre>
                        <div className="mt-4 text-sm text-gray-600">
                          <p>Language: {fileContent.language || 'Unknown'}</p>
                          <p>Size: {(fileContent.size / 1024).toFixed(2)} KB</p>
                        </div>
                      </div>
                    ) : (
                      <div className="p-4 text-center text-gray-500">
                        Failed to load file content
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div className="p-8 text-center text-gray-500">
                  <p className="text-lg">Select a file to view its contents</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
