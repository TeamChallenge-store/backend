import { FC, ReactNode, useState } from 'react';
import { TopHeader } from '../TopHeader';
import { Navbar } from '../Navbar';
import { Icons } from '../Icons';
import { Logo } from '~entities/logo';
import { Icon } from '~shared/ui/Icon';
import { BurgerMenu } from '../BurgerMenu';

import css from './HeaderDefault.module.scss';

type THeaderDefaultProps = {
  searchSlot?: ReactNode;
};

const HeaderDefault: FC<THeaderDefaultProps> = ({ searchSlot }) => {
  const [openBurger, setOpenBurger] = useState(false);

  const handleBurger = () => {
    setOpenBurger(!openBurger);
  };

  return (
    <>
      <TopHeader />
      <div className="container">
        <div className={css.inner}>
          <div className={css.leftHeader}>
            <Logo type="header" className={css.logo} />
            <Navbar />
            <Icon type="burger" btnStyle={css.burger} onClick={handleBurger} />
          </div>
          <div className={css.rightHeader}>{searchSlot}</div>
          <Icons />
        </div>
      </div>
      <BurgerMenu isOpen={openBurger} setIsOpen={handleBurger} />
    </>
  );
};

export { HeaderDefault };
