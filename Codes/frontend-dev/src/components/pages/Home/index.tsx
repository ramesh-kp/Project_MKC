import { HomeDashboard } from '@components/ui/Home/Home';

export const HomePage = ({ type }: { type: string }) => (
  <HomeDashboard {...{ type }} />
);
