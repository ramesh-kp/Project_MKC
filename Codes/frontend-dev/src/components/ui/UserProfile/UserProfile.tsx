import { Dispatch, FC, SetStateAction } from 'react';
import { useSession } from '@lib/useSession';
export interface ProfileSectionProps {
  setChangePassword: Dispatch<SetStateAction<boolean>>;
}

export const ProfileSection: FC<ProfileSectionProps> = ({
  setChangePassword,
}) => {
  const { state } = useSession();
  const { currentUser } = state;

  return (
    <div className="w-full">
      <h2 className="text-2xl font-semibold py-3">Profile</h2>

      <input
        type="text"
        className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0"
        value={currentUser.name}
      />
      <input
        type="text"
        className="w-full py-2 mb-4 border-0 border-b-2 focus-visible:outline-0"
        value={currentUser.email}
      />
      <button
        type="button"
        className="inline-block mt-2 px-5 py-2 rounded-md text-slate-700 bg-gray-200 hover:text-black hover:bg-slate-300"
        onClick={() => setChangePassword(true)}
      >
        Change Password
      </button>
    </div>
  );
};
