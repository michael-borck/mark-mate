import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { User, ApiResponse } from './types';

interface UserCardProps {
  user: User;
  onUserClick?: (user: User) => void;
  isSelected?: boolean;
  className?: string;
}

const UserCard: React.FC<UserCardProps> = ({ 
  user, 
  onUserClick, 
  isSelected = false, 
  className = '' 
}) => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [userDetails, setUserDetails] = useState<User | null>(null);

  useEffect(() => {
    if (isSelected && !userDetails) {
      fetchUserDetails();
    }
  }, [isSelected, userDetails]);

  const fetchUserDetails = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`/api/users/${user.id}`);
      const data: ApiResponse<User> = await response.json();
      setUserDetails(data.result);
    } catch (error) {
      console.error('Failed to fetch user details:', error);
    } finally {
      setIsLoading(false);
    }
  }, [user.id]);

  const displayName = useMemo(() => {
    return `${user.firstName} ${user.lastName}`;
  }, [user.firstName, user.lastName]);

  const handleCardClick = useCallback(() => {
    if (onUserClick) {
      onUserClick(user);
    }
  }, [onUserClick, user]);

  const cardClasses = useMemo(() => {
    return [
      'user-card',
      isSelected && 'user-card--selected',
      isLoading && 'user-card--loading',
      className
    ].filter(Boolean).join(' ');
  }, [isSelected, isLoading, className]);

  return (
    <div 
      className={cardClasses}
      onClick={handleCardClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          handleCardClick();
        }
      }}
    >
      <header className="user-card__header">
        <img 
          src={user.avatar || '/default-avatar.png'} 
          alt={`${displayName}'s avatar`}
          className="user-card__avatar"
        />
        <div className="user-card__info">
          <h3 className="user-card__name">{displayName}</h3>
          <p className="user-card__email">{user.email}</p>
        </div>
      </header>
      
      {isSelected && (
        <section className="user-card__details">
          {isLoading ? (
            <div className="user-card__loading">
              <span>Loading user details...</span>
            </div>
          ) : userDetails ? (
            <>
              <div className="user-card__field">
                <label>Department:</label>
                <span>{userDetails.department}</span>
              </div>
              <div className="user-card__field">
                <label>Role:</label>
                <span>{userDetails.role}</span>
              </div>
              {userDetails.bio && (
                <div className="user-card__field">
                  <label>Bio:</label>
                  <p>{userDetails.bio}</p>
                </div>
              )}
            </>
          ) : (
            <div className="user-card__error">
              Failed to load user details
            </div>
          )}
        </section>
      )}
      
      <footer className="user-card__footer">
        <small>Last active: {new Date(user.lastActive).toLocaleDateString()}</small>
      </footer>
    </div>
  );
};

UserCard.displayName = 'UserCard';

export default React.memo(UserCard);