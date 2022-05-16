import { useState, memo, FC, Dispatch, SetStateAction } from 'react';
import Image from 'next/image';
import { useSession } from '@lib/useSession';
import DownArrow from 'assets/down_arrow.png';
import Logo from 'assets/logo.svg';
import { ProfilePage } from '@components/pages/Profile';
import { globalVariables, PageNames } from '@lib/common';
import { UserRoleType } from '@api/graphql';

export interface HeaderComponentProps {
  dashboardType: string;
  setDasboardType: Dispatch<SetStateAction<string>>;
  pathName: string;
}
const HeaderComponent: FC<HeaderComponentProps> = ({
  setDasboardType,
  dashboardType,
  pathName,
}) => {
  const [profileFlag, setProfileFlag] = useState<boolean>(false);
  const { state } = useSession();
  const { currentUser } = state;

  const menuVisible =
    pathName === globalVariables.home &&
    currentUser.role === UserRoleType.Admin;

  return (
    <>
      <div className="top-0 fixed navbar px-2 py-2 bg-base-100 lg:px-5 lg:py-2 z-30">
        <div className="navbar-start">
          <div className="dropdown">
            <label className="px-3 btn btn-ghost lg:hidden">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h8m-8 6h16"
                />
              </svg>
            </label>
            <ul
              tabIndex={0}
              className="mt-3 p-2 shadow menu menu-compact dropdown-content bg-base-100 rounded-box w-52"
            >
              <li>
                <label>{globalVariables.water}</label>
              </li>
              <li>
                <label>{globalVariables.power}</label>
              </li>
              {currentUser.role !== globalVariables.tenant && (
                <li>
                  <label>{globalVariables.sewage}</label>
                </li>
              )}
            </ul>
          </div>
          <label className="w-32 block float-left">
            <Image src={Logo} className="max-w-full" alt="logo" />
          </label>
        </div>
        {menuVisible && (
          <div className="navbar-center hidden lg:flex">
            <ul className="menu menu-horizontal p-0">
              <li className="mx-1">
                <button
                  className={
                    dashboardType === globalVariables.water
                      ? 'px-5 py-1 bg-sky-600 rounded-2xl text-white font-medium'
                      : 'px-5 py-1 font-medium'
                  }
                  onClick={() => setDasboardType(globalVariables.water)}
                >
                  {globalVariables.water}
                </button>
              </li>
              <li className="mx-1">
                <button
                  className={
                    dashboardType === globalVariables.power
                      ? 'px-5 py-1 bg-sky-600 rounded-2xl text-white font-medium'
                      : 'px-5 py-1 font-medium'
                  }
                  onClick={() => setDasboardType(globalVariables.power)}
                >
                  {globalVariables.power}
                </button>
              </li>
              {currentUser.role !== globalVariables.tenant && (
                <li className="mx-1">
                  <button
                    className={
                      dashboardType === 'Sewage'
                        ? 'px-5 py-1 bg-sky-600 rounded-2xl text-white font-medium'
                        : 'px-5 py-1 font-medium'
                    }
                    onClick={() => setDasboardType('Sewage')}
                  >
                    {globalVariables.sewage}
                  </button>
                </li>
              )}
            </ul>
          </div>
        )}
        <div className="navbar-end">
          <label
            className="block float-right flex hover:bg-gray-200 pl-2 rounded-full lg:pl-5"
            onClick={() => setProfileFlag(!profileFlag)}
          >
            <div className="pt-1 text-base text-current lg:pt-3">
              {currentUser.name}
              <Image
                src={DownArrow}
                className="inline-block ml-3"
                alt="downArrow"
              />
            </div>
            <div className="rounded-full bg-green-200 w-8 h-8 pt-1 text-center ml-2 bg-fuchsia-800 text-white uppercase text-1xl font-semibold leading-relaxed lg:w-12 lg:h-12 lg:ml-4 lg:text-3xl">
              {currentUser.name?.charAt(0)}
            </div>
          </label>
        </div>
      </div>
      {profileFlag && <ProfilePage {...{ setProfileFlag }} />}
    </>
  );
};

export const Header = memo(HeaderComponent);
