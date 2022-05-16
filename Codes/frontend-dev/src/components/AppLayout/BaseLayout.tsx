import { FC, useState } from 'react';
import { useRouter } from 'next/router';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { HomePage } from '@components/pages/Home';
import { globalVariables, PageNames } from '@lib/common';
import { useSession } from '@lib/useSession';
import { UserRoleType } from '@api/graphql';
import { TenantDashboard } from '@components/pages/Tenants/TenantDashboard';

export const BaseAppLayout: FC = ({ children }) => {
  type pageType = {
    type: {
      name: string;
    };
  };
  const router = useRouter();
  const { state } = useSession();
  const { currentUser } = state;
  const page: pageType = children as pageType;
  const [dashboardType, setDasboardType] = useState<string>(
    globalVariables.water,
  );

  const pathName = router.pathname.toLocaleLowerCase().replace(/\//g, '');
  const headerVisibility = Boolean(
    pathName === 'login' ||
      pathName === '' ||
      pathName === 'forgot-password' ||
      pathName === 'reset-password',
  );

  return (
    <div className="min-h-full relative">
      {headerVisibility ? (
        page
      ) : (
        <>
          <Header {...{ dashboardType, setDasboardType, pathName }} />
          <main className="mt-16  bg-gray-100">
            <Sidebar />
            {/* content start */}
            <div className="ml-12 p-3 h-screen overscroll-y-auto md:p-5 lg:ml-20 lg:p-10">
              {currentUser.role === UserRoleType.Tenant ? (
                <TenantDashboard />
              ) : pathName === globalVariables.home ? (
                <HomePage type={dashboardType} />
              ) : (
                page
              )}
            </div>
            {/* content end */}
          </main>
        </>
      )}
    </div>
  );
};
