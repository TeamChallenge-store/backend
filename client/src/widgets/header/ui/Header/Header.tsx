import { ReactNode, FC } from 'react';
import { HeaderDefault } from '../HeaderDefault';
import { HeaderMini } from '../HeaderMini';
import { useCheckLocation } from '~features/check-location/checkLocation';
import css from './Header.module.scss';
// eslint-disable-next-line max-len
import { SuccessSubscribeMessage } from '~shared/ui/SuccessSubscribeMessage/SuccessSubscribeMessage';

type THeaderProps = {
  searchSlot?: ReactNode;
};

const Header: FC<THeaderProps> = ({ searchSlot }) => {
  const { isCheckoutPage, isThankYou, isError } = useCheckLocation();

  return (
    <header className={css.header}>
      {!isCheckoutPage && !isThankYou && !isError ? (
        <HeaderDefault searchSlot={searchSlot} />
      ) : (
        <HeaderMini />
      )}
      <SuccessSubscribeMessage />
    </header>
  );
};

export { Header };
