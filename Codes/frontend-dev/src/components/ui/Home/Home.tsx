import { useRouter } from 'next/router';
import { globalVariables } from '@lib/common';
import { useSession } from '@lib/useSession';
import { PowerDashboard } from './PowerDashboard';
import { SewageDashboard } from './SewageDashboard';
import { WaterDashboard } from './WaterDashboard';

export const HomeDashboard = ({ type }: { type: string }) => {
  const { state } = useSession();
  const { currentUser } = state;
  const route = useRouter();

  if (currentUser.role === undefined) route.push('/login');
  if (type === globalVariables.power) return <PowerDashboard />;
  if (type === 'Sewage' && currentUser.role !== globalVariables.tenant)
    return <SewageDashboard />;
  return <WaterDashboard />;
};
