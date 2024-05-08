import { useNavigate } from 'react-router-dom';
import categoriesData from '../../categories';

import css from './CategoriesBanner.module.scss';
import { CustomButton } from '~shared/ui/CustomButton';

const CategoriesBanner = () => {
  const navigate = useNavigate();

  const productLink = (index: number) => {
    return categoriesData[index].linkToProduct;
  };

  const handleCardAction = (
    link: string,
    event?: React.KeyboardEvent<HTMLDivElement>,
  ) => {
    if (!event || event.key === 'Enter' || event.key === ' ') {
      navigate(link);
    }
  };

  return (
    <div className={css.cardContainer}>
      <div className={css.leftContainer}>
        <div className={css.cardHoverEffect}>
          <div
            key={categoriesData[0].id}
            className={css.card}
            onClick={() => handleCardAction(productLink(0))}
            role="button"
            onKeyDown={event => handleCardAction(productLink(0), event)}
            tabIndex={0}
          >
            <img
              src={categoriesData[0].backgroundImage}
              alt={categoriesData[0].title}
              className={css.cardImage}
            />
            <div className={css.content}>
              <div className={css.boxLeftContent}>
                <h3 className={css.title}>{categoriesData[0].title}</h3>
                <p className={css.subtitle}>{categoriesData[0].subtitle}</p>
              </div>
              <CustomButton
                bgColor="white"
                className={css.cardButton}
                to={categoriesData[0].linkToProduct}
                onClick={e => e.stopPropagation()}
              >
                See more
                <svg
                  width="25"
                  height="24"
                  viewBox="0 0 25 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    // eslint-disable-next-line max-len
                    d="M8.64239 6.43312L18.1442 7.34961L17.2277 16.8515M17.4207 7.94582L6.8577 16.6504"
                    stroke="rgba(17, 29, 19, 1)"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </CustomButton>
              <CustomButton
                bgColor="white"
                className={`${css.cardButton} ${css.cardButtonArrowFirst}`}
                to={categoriesData[0].linkToProduct}
                onClick={e => e.stopPropagation()}
              >
                <svg
                  width="25"
                  height="24"
                  viewBox="0 0 25 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    // eslint-disable-next-line max-len
                    d="M8.64239 6.43312L18.1442 7.34961L17.2277 16.8515M17.4207 7.94582L6.8577 16.6504"
                    stroke="rgba(17, 29, 19, 1)"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </CustomButton>
            </div>
          </div>
        </div>
      </div>

      <div className={css.rightContainer}>
        {categoriesData.slice(1).map((product, index) => (
          <div className={css.cardHoverEffect} key={product.id}>
            <div
              className={css.card}
              onClick={() => handleCardAction(productLink(index + 1))}
              role="button"
              tabIndex={0}
              onKeyDown={e => handleCardAction(productLink(index + 1), e)}
            >
              <img
                src={categoriesData[index + 1].backgroundImage}
                alt={product.title}
                className={css.cardImage}
              />
              <div className={css.content}>
                <h3 className={css.title}>{product.title}</h3>
                <CustomButton
                  bgColor="white"
                  className={css.cardButton}
                  to={product.linkToProduct}
                  onClick={e => e.stopPropagation()}
                >
                  <svg
                    width="25"
                    height="24"
                    viewBox="0 0 25 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      // eslint-disable-next-line max-len
                      d="M8.64239 6.43312L18.1442 7.34961L17.2277 16.8515M17.4207 7.94582L6.8577 16.6504"
                      stroke="rgba(17, 29, 19, 1)"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </CustomButton>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export { CategoriesBanner };
