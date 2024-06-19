const TOUR_OPTIONS_KEY = 'tour-options';
const CHAT_FIRST_SHOW_KEY = 'show-chat-first-time';
const KNOWLEDGE_CHAT_FIRST_SHOW_KEY = 'show-knowledge-chat-first-time';
const MULTI_SOURCE_CHAT_FIRST_SHOW_KEY = 'show-multi-source-chat-first-time';

function getLocalStorageOptions() {
  return JSON.parse(localStorage.getItem(TOUR_OPTIONS_KEY)) || {};
}

function saveLocalStorageOptions(options) {
  localStorage.setItem(TOUR_OPTIONS_KEY, JSON.stringify(options));
}

export function hasChatBeenShownFirstTime() {
  const tourOptions = getLocalStorageOptions();
  return !!tourOptions[CHAT_FIRST_SHOW_KEY];
}

export function hasKnowledgeChatBeenShownFirstTime() {
  const tourOptions = getLocalStorageOptions();
  return !!tourOptions[KNOWLEDGE_CHAT_FIRST_SHOW_KEY];
}

export function setChatFirstShowStatus(hasShown) {
  const tourOptions = getLocalStorageOptions();
  tourOptions[CHAT_FIRST_SHOW_KEY] = hasShown;
  saveLocalStorageOptions(tourOptions);
}

export function setKnowledgeChatFirstShowStatus(hasShown) {
  const tourOptions = getLocalStorageOptions();
  tourOptions[KNOWLEDGE_CHAT_FIRST_SHOW_KEY] = hasShown;
  saveLocalStorageOptions(tourOptions);
}

export function setMultiSourceChatFirstShowStatus(hasShown) {
  const tourOptions = getLocalStorageOptions();
  tourOptions[MULTI_SOURCE_CHAT_FIRST_SHOW_KEY] = hasShown;
  saveLocalStorageOptions(tourOptions);
}

export function hasMultiSourceChatBeenShownFirstTime() {
  const tourOptions = getLocalStorageOptions();
  return !!tourOptions[MULTI_SOURCE_CHAT_FIRST_SHOW_KEY];
}
