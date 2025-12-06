import { render, screen } from '@testing-library/react';
import Home from '../page';

// Mock the api module
jest.mock('@/lib/api', () => ({
  api: {
    get: jest.fn().mockResolvedValue({
      data: { items: [] },
    }),
  },
}));

describe('Home Page', () => {
  it('renders main heading', () => {
    render(<Home />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('FastAPI + Next.js');
  });

  it('renders backend section', () => {
    render(<Home />);
    const backendHeading = screen.getByRole('heading', { level: 2 });
    expect(backendHeading).toBeInTheDocument();
  });

  it('displays getting started section', () => {
    render(<Home />);
    const gettingStartedHeading = screen.getByRole('heading', {
      name: /getting started/i,
    });
    expect(gettingStartedHeading).toBeInTheDocument();
  });
});
