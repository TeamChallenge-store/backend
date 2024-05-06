import { FC, useState } from 'react';
import { Link } from 'react-router-dom';
import { navigationData } from '../Navbar/config/navigationData';
import arrowRight from '../../NavigationIcons/arrowRight.svg';
import arrowLeft from '../../NavigationIcons/arrowLeft.svg';
import basketIcon from '../../NavigationIcons/basket.svg';

import css from './BurgerNavigation.module.scss';

type TBurgerNavigationProps = {
  className: string;
  setIsOpen: () => void;
};

type Category = {
  title: string;
  url: string;
  submenu?: {
    title: string;
    url: string;
  }[];
};

const BurgerNavigation: FC<TBurgerNavigationProps> = ({
  className,
  setIsOpen,
}) => {
  const [activeCategory, setActiveCategory] = useState<Category | null>(null);
  const [showNavigation, setShowNavigation] = useState<boolean>(true);

  const handleCategoryClick = (category: Category) => {
    setActiveCategory(category);
  };

  const handleBackClick = () => {
    setActiveCategory(null);
  };

  return (
    <>
      {showNavigation && (
        <ul className={`${css.navigation} ${className}`}>
          <div className={css.item}>
            <Link
              to="/allPropducts"
              onClick={() => {
                setIsOpen();
              }}
              className={css.navLink}
            >
              <img src={basketIcon} alt="basket" className={css.icon} />
              See all
            </Link>
          </div>
          {navigationData.map(category => (
            <li key={category.title} className={css.item}>
              <Link
                to={category.url}
                onClick={() => {
                  setIsOpen();
                }}
                className={css.navLink}
              >
                <img
                  src={category.icon}
                  alt={category.title}
                  className={css.icon}
                />
                {category.title}
              </Link>
              {category.submenu && (
                <button
                  onClick={() => {
                    handleCategoryClick(category);
                    setShowNavigation(false);
                  }}
                  className={css.arrow}
                  type="button"
                >
                  <img
                    src={arrowRight}
                    alt="to categories"
                    className={css.arrowRight}
                  />
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
      {activeCategory && (
        <div className={css.subMenu}>
          <button
            onClick={() => {
              handleBackClick();
              setShowNavigation(true);
            }}
            className={css.arrowBack}
            type="button"
          >
            <img src={arrowLeft} alt="turn back" className={css.arrowLeft} />
            Back
          </button>
          <h2 className={css.subtitle}>{activeCategory.title}</h2>
          <ul>
            {
              // eslint-disable-next-line operator-linebreak
              activeCategory.submenu &&
                activeCategory.submenu.map(subCategory => (
                  <li key={subCategory.title} className={css.item}>
                    <Link
                      to={subCategory.url}
                      className={css.navLink}
                      onClick={() => setIsOpen()}
                    >
                      {subCategory.title}
                    </Link>
                  </li>
                ))
            }
          </ul>
        </div>
      )}

      {showNavigation && (
        <ul className={css.info}>
          <li>
            <Link to="/delivery" onClick={() => setIsOpen()}>
              Delivery
            </Link>
          </li>
          <li>
            <Link to="/payment" onClick={() => setIsOpen()}>
              Payment
            </Link>
          </li>
          <li>
            <Link to="/contacts" onClick={() => setIsOpen()}>
              Contacts
            </Link>
          </li>
          <li>
            <Link to="/aboutUs" onClick={() => setIsOpen()}>
              About us
            </Link>
          </li>
        </ul>
      )}
    </>
  );
};

export { BurgerNavigation };
