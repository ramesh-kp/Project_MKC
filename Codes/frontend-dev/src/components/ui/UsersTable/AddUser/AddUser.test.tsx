import React from 'react'
import { fireEvent, render } from '@testing-library/react'
import { AddUserForm, AddUserProps } from './AddUser'

const renderAdminUserProfile = (
  props?: React.FunctionComponent<AddUserProps>,
) => {
  const defaultProps = {
    register: jest.fn(),
    errors: {},
    addUser: jest.fn(),
  }
  return render(
    <AddUserForm
      handleClose={function (): void {
        throw new Error('Function not implemented.')
      }}
      buttonLoading={false}
      {...defaultProps}
      {...props}
    />,
  )
}

describe('testing all the elements in the  Page', () => {
  it('initial loading data', () => {
    const { getByTestId } = renderAdminUserProfile()
    expect(getByTestId('name')).toHaveValue('')
    expect(getByTestId('email')).toHaveValue('')

    expect(getByTestId('submit-button')).toBeInTheDocument()
    fireEvent.click(getByTestId('submit-button'))
  })
})
