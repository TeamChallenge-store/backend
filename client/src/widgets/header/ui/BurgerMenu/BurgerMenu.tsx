import { FC } from 'react';
import cn from 'classnames';
import { Icon } from '~shared/ui/Icon';
import { Logo } from '~entities/logo';
import { Socials } from '../Socials';
import { BurgerNavigation } from '../BurgerNavigation';

import css from './BurgerMenu.module.scss';

type TBurgerMenuProps = {
  isOpen: boolean;
  setIsOpen: () => void;
};

const BurgerMenu: FC<TBurgerMenuProps> = ({ isOpen, setIsOpen }) => {
  return (
    <>
      <div className={cn(css.menu, { [css.animating]: isOpen })}>
        <div className={css.menuTop}>
          <Logo type="header" className={css.burgerLogo} onClick={setIsOpen} />
          <Icon type="close" onClick={setIsOpen} className={css.closeBtn} />
        </div>
        <BurgerNavigation className={css.navigation} setIsOpen={setIsOpen} />
        <Socials />
      </div>
    </>
  );
};

export { BurgerMenu };
