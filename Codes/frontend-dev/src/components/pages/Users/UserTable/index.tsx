import { useState } from 'react';
import Image from 'next/image';
import { useQueryClient } from 'react-query';
import TablePagination from '@components/ui/CommonPage/TablePagination';
import {
  InputMaybe,
  QueryMode,
  UpdateUserMutation,
  UserRoleType,
  UsersQueryVariables,
  UserStatusType,
  useUpdateUserMutation,
  useUsersQuery,
} from '@api/graphql';
import graphQLClient from '@lib/useGQLQuery';
import { UserListView } from 'ui/UsersTable/UsersListView';
import AddUserPage from '../AddUser';
import UserIcon from 'assets/user-white.png';
import SearchIcon from 'assets/search_icon.png';
import { messages, orderAsc, status, UsersType } from '@lib/common';
import CustomizedSnackbars from 'ui/CommonPage/SnackBar/Snackbar';
import { ApiLoader } from '@components/ui/CommonPage/ApiLoader';
import { ErrorPage } from '@components/ui/CommonPage/ErrorPage/ErrorPage';
import { NoRecords } from '@components/ui/CommonPage/NoRecords/NoRecords';
import { ConfirmationMessage } from '@components/ui/CommonPage/ConfirmationMessage';
import { useSession } from '@lib/useSession';
import { useRouter } from 'next/router';

export const UserList = () => {
  const tableTake = 10;
  const queryClient = useQueryClient();
  const { state } = useSession();
  const { currentUser } = state;
  const route = useRouter();

  if (currentUser.role === undefined) route.push('/login');

  const searchDefault = {
    mode: 'insensitive' as InputMaybe<QueryMode> | undefined,
    contains: '',
  };

  const whereCondition = {
    OR: [
      {
        name: searchDefault,
      },
      {
        phone: searchDefault,
      },
      {
        email: searchDefault,
      },
      {
        tenant: {
          name: searchDefault,
        },
      },
    ],
    role: {
      equals: UserRoleType.Tenant,
    },
  };

  const queryVariables = {
    take: tableTake,
    skip: 0,
    usersCountWhere2: whereCondition,
    where: whereCondition,
    orderBy: orderAsc,
  };
  const confirmationText = 'Do you want to change the status of the user ?';
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [messageType, setMessageType] = useState<string>('');
  const [open, setOpen] = useState<boolean>(false);
  const [searchItem, setSearchItem] = useState<string>('');
  const [pageSelected, setPageSelected] = useState<number>(1);
  const [addUserFlag, setAddUserFlag] = useState<boolean>(false);
  const [loader, setLoader] = useState<boolean>(false);
  const [editData, setEditData] = useState<UsersType>();
  const [confirmationFlag, setConfirmationFlag] = useState<boolean>(false);
  const [action, setAction] = useState<string>('');
  const [actionId, setActionId] = useState<string>('');
  const [variables, setVaribles] =
    useState<UsersQueryVariables>(queryVariables);
  const { data, isLoading, isError } = useUsersQuery(
    graphQLClient(),
    variables,
  );
  const totaldata = data?.usersCount;
  const updateMutation = useUpdateUserMutation<UpdateUserMutation>(
    graphQLClient(),
  );

  const pagination = async (value: number) => {
    setPageSelected(value + 1);
    const skipvalue = value * tableTake;
    setVaribles(prev => {
      return { ...prev, skip: skipvalue };
    });
  };

  const searchItems = () => {
    const convertedSearchItem = {
      mode: 'insensitive' as InputMaybe<QueryMode> | undefined,
      contains: searchItem,
    };

    const condition = {
      OR: [
        {
          name: convertedSearchItem,
        },
        {
          phone: convertedSearchItem,
        },
        {
          email: convertedSearchItem,
        },
        {
          tenant: {
            name: convertedSearchItem,
          },
        },
      ],
      role: {
        equals: UserRoleType.Tenant,
      },
    };

    setVaribles(prev => {
      return {
        ...prev,
        where: condition,
        usersCountWhere2: condition,
        skip: 0,
      };
    });
    setPageSelected(1);
  };

  const actionConfirm = (action: string, userId: string) => {
    setConfirmationFlag(true);
    setAction(action);
    setActionId(userId);
  };

  const closeConfirmation = () => {
    setConfirmationFlag(false);
    setAction('');
    setActionId('');
  };

  const actionSubmit = async () => {
    try {
      setConfirmationFlag(false);
      setLoader(true);
      const variable = {
        where: {
          id: actionId,
        },
        data: {
          status: action as UserStatusType,
        },
      };
      await updateMutation.mutateAsync(variable);
      queryClient.invalidateQueries();
      setErrorMessage(
        action === UserStatusType.Inactive
          ? messages.userDeactivatedMessage
          : messages.userActivatedMessage,
      );
      setMessageType(status.success);
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      setErrorMessage(messages.commonError);
      setMessageType(status.error);
    } finally {
      setOpen(true);
      setLoader(false);
      setAction('');
      setActionId('');
    }
  };

  if (currentUser.role === undefined) route.push('/login');
  if (isLoading || loader) return <ApiLoader />;
  if (isError) return <ErrorPage />;

  return (
    <>
      <CustomizedSnackbars
        {...{ open, setOpen }}
        message={errorMessage}
        type={messageType}
      />
      <div className="p-6 bg-white rounded-lg">
        <h1 className="inline-block text-2xl font-semibold">Users</h1>
        <div className="float-right flex">
          <div className="relative mr-4 h-10 overflow-hidden rounded-md">
            <input
              value={searchItem}
              type="text"
              className="mr-5 px-3 py-2 bg-slate-200 focus-visible:outline-0 text-md font-medium text-gray-700"
              placeholder="Search here..."
              onChange={e => setSearchItem(e.target.value)}
              onKeyDown={e => {
                if (e.key === 'Enter') searchItems();
              }}
            />
            <button
              type="button"
              className="bg-sky-600 px-3 pt-1 h-10 absolute top-0 right-0 hover:bg-sky-700"
              onClick={() => searchItems()}
            >
              <Image
                src={SearchIcon}
                className="inline-block search_icon"
                alt=""
              />
            </button>
          </div>
          <button
            type="button"
            className="h-10 bg-sky-600 float-right text-white px-4 pt-2 rounded-md text-md font-semibold hover:bg-sky-700"
            onClick={() => setAddUserFlag(true)}
          >
            <Image src={UserIcon} className="inline-block mr-1" alt="user" />{' '}
            Add User
          </button>
        </div>
        <div className="clear-both" />
        {data?.users?.length === 0 ? (
          <NoRecords />
        ) : (
          <div className="flex flex-col">
            <div className="-my-2 mt-4 sm:-mx-6 lg:-mx-8">
              <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
                <UserListView
                  tableData={data?.users}
                  {...{ setAddUserFlag, setEditData, actionConfirm }}
                />
                <TablePagination
                  totaldata={totaldata ?? 0}
                  {...{ pagination, tableTake, pageSelected }}
                />
              </div>
            </div>
          </div>
        )}
      </div>
      {addUserFlag && (
        <AddUserPage
          {...{
            setAddUserFlag,
            editData,
            setEditData,
            setOpen,
            setErrorMessage,
            setMessageType,
          }}
        />
      )}
      {confirmationFlag && (
        <ConfirmationMessage
          {...{ closeConfirmation, confirmationText }}
          confirmedAction={actionSubmit}
        />
      )}
    </>
  );
};
