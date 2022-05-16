import {
  createContext,
  memo,
  ReactNode,
  useContext,
  useEffect,
  useReducer,
} from 'react';
import { useRouter } from 'next/router';
import graphQLClient from './useGQLQuery';
import {
  useAuthenticatedItemQuery,
  useLogoutMutation,
  UserRoleType,
  UserStatusType,
} from '../api/graphql';
import { ApiLoader } from '@components/ui/CommonPage/ApiLoader';
import { ErrorPage } from '@components/ui/CommonPage/ErrorPage/ErrorPage';
import { dateBeforeOneWeek, todayDate } from './common';
import moment from 'moment';

export type CurrentUser = {
  __typename?: 'User';
  id: string;
  name?: string;
  email?: string;
  role?: UserRoleType;
  status?: UserStatusType;
  userUploadsCount?: number;
  password?: {
    __typename?: 'PasswordState';
    isSet: boolean;
  };
  tenant?: {
    __typename?: 'Tenant';
    id: string;
    name: string;
    status?: string;
  };
};

export type DateRange = {
  from: string;
  to: string;
};
type Action =
  | {
      type: 'saveUserLogin';
      user: CurrentUser;
    }
  | {
      type: 'dateSelection';
      dateRange: DateRange;
    }
  | {
      type: 'logout';
    };

type Dispatch = (action: Action) => void;

type State = {
  currentUser: CurrentUser;
  dateRange: DateRange;
};
type SessionProviderProps = { children: ReactNode };

const SessionStateContext = createContext<
  { state: State; dispatch: Dispatch } | undefined
>(undefined);
let logout: any;

function useSession(login: boolean = false) {
  const context = useContext(SessionStateContext);
  if (context === undefined) {
    throw new Error('useSession must be used within a SessionProvider');
  }
  return context;
}

function sessionReducer(state: State, action: Action) {
  switch (action.type) {
    case 'saveUserLogin': {
      return {
        currentUser: action.user,
        dateRange: state.dateRange,
      };
    }

    case 'logout': {
      logout?.mutate();
      return {
        currentUser: {} as CurrentUser,
        dateRange: state.dateRange,
      };
    }

    case 'dateSelection': {
      return {
        currentUser: state.currentUser,
        dateRange: action.dateRange,
      };
    }
    default: {
      throw new Error(`Unhandled action type: ${action}`);
    }
  }
}

const SessionLoaderComponent = ({ children }: SessionProviderProps) => {
  const router = useRouter();
  logout = useLogoutMutation(graphQLClient());
  const currentUser = {} as CurrentUser;
  const dateRange = {
    from: moment(dateBeforeOneWeek).format('YYYY-MM-DD'),
    to: moment(todayDate).format('YYYY-MM-DD'),
  } as DateRange;

  const [state, dispatch] = useReducer(sessionReducer, {
    currentUser,
    dateRange,
  });
  const value = { state, dispatch };
  const { data, isLoading, isError } = useAuthenticatedItemQuery(
    graphQLClient(),
    {},
  );
  useEffect(() => {
    if (data?.authenticatedItem) {
      dispatch({
        type: 'saveUserLogin',
        user: data.authenticatedItem as CurrentUser,
      });
    }
    const pathName = router.pathname.toLocaleLowerCase().replace(/\//g, '');
    if (
      pathName === 'login' ||
      pathName === 'forgot-password' ||
      pathName === 'reset-password'
    ) {
      if (data?.authenticatedItem) router.push('/home');
      return;
    }
    if (data?.authenticatedItem === null && !isLoading) {
      dispatch({ type: 'logout' });
      router.push('/login');
    }
  }, [data]);

  if (isLoading) return <ApiLoader />;
  if (isError) return <ErrorPage />;

  return (
    <SessionStateContext.Provider value={value}>
      {children}
    </SessionStateContext.Provider>
  );
};

const SessionLoader = memo(SessionLoaderComponent);
export { SessionLoader, useSession };
