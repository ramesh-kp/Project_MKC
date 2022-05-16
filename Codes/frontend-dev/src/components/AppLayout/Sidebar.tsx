import { useState } from 'react';
import { useRouter } from 'next/router';
import Image from 'next/image';
import Home from 'assets/home.png';
import HomeActive from 'assets/home_active.png';
import UserActive from 'assets/user_active.png';
import TenantInactive from 'assets/tenants.png';
import SensorsInactive from 'assets/sensors.png';
import Settings from 'assets/setting.png';
import SettingsActive from 'assets/setting_active.png';
import UserInactive from 'assets/user.png';
import TenantActive from 'assets/tenants_active.png';
import SensorsActive from 'assets/sensors_active.png';
import { globalVariables, PageNames } from '@lib/common';
import { useSession } from '@lib/useSession';

export const Sidebar = () => {
  const router = useRouter();
  const { state } = useSession();
  const { currentUser } = state;
  const menuItems =
    currentUser.role === globalVariables.tenant
      ? [PageNames.home]
      : [PageNames.home, PageNames.user, PageNames.tenant, PageNames.sensors];
  const [selectedMenu, setSelectedMenu] = useState<string>(PageNames.home);
  const imagePath = (item: string) => {
    switch (item) {
      case PageNames.home:
        if (selectedMenu === item) return HomeActive;
        else return Home;
      case PageNames.user:
        if (selectedMenu === item) return UserActive;
        else return UserInactive;

      case PageNames.tenant:
        if (selectedMenu === item) return TenantActive;
        else return TenantInactive;

      case PageNames.sensors:
        if (selectedMenu === item) return SensorsActive;
        else return SensorsInactive;
      case PageNames.settings:
        if (selectedMenu === item) return SettingsActive;
        else return Settings;
      default:
        return HomeActive;
    }
  };
  const menuSelection = (value: string) => {
    setSelectedMenu(value);
    switch (value) {
      case PageNames.home:
        return router.push('/home');
      case PageNames.user:
        return router.push('/user');
      case PageNames.tenant:
        return router.push('/tenant');
      case PageNames.sensors:
        return router.push('/sensor');
      case PageNames.settings:
        return router.push('/settings');
      default:
        return router.push('/home');
    }
  };
  return (
    <div className="fixed w-12 h-screen bg-white text-center lg:w-20">
      <ul className="pt-4  text-center">
        {menuItems.map((path: string) => (
          <li key={path} onClick={() => menuSelection(path)}>
            <label className="w-full inline-block py-4 hover:bg-gray-100 lg:py-5">
              <Image
                src={imagePath(path) as string | StaticImageData}
                className="inline-block cursor-pointer"
                alt="Menu"
              />
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
};
