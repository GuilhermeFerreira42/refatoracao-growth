//CONSTANTES
var WCOOKIE_CONSENT = "_cookie_consent";
var WCOOKIE_CONSENT_PERFORMANCE = "_cookie_consent_performance";
var WCOOKIE_CONSENT_MARKETING   = "_cookie_consent_marketing";
var WCOOKIE_CONSENT_FUNCTIONAL  = "_cookie_consent_functional";

//VARIÁVEIS
var wCookieConsentBar;
var wCookieConsentModal;
var wCookieConsentCheckPerformance;
var wCookieConsentCheckMarketing;
var wCookieConsentCheckFunctional;

//TEXTOS
var wCookieConsentTexts = {
  textBar: 'Clicando em "Aceito todos os Cookies", você concorda com o armazenamento de cookies no seu dispositivo para melhorar a experiência e navegação no site.',

  strictTitle: 'Cookies necessários',
  strictDescription: 'Estes cookies são aqueles necessários para o site funcionar e não podem ser desligados em nossos sistemas. Eles geralmente são definidos apenas em resposta às ações feitas por você, como por exemplo, definir suas preferências de privacidade, fazer login ou preencher formulários. Caso queira, pode configurar seu navegador para bloqueá-lo ou alertá-lo sobre esses cookies, mas algumas partes do site podem não funcionar de forma adequada.',

  performanceTitle: 'Cookies de desempenho',
  performanceDescription: 'Os cookies de desempenho fornecem informações sobre como este site está sendo usado para que possamos melhorar a experiência do usuário. Os dados capturados são agregados e anonimizados.',

  functionalTitle: 'Cookies funcionais',
  functionalDescription: 'Os cookies funcionais ajustam o site a serviços de terceiros como vínculo ao seu perfil em redes sociais, comentários, chatbots, etc.',

  marketingTitle: 'Cookies de marketing',
  marketingDescription: 'Os cookies de marketing fornecem informações sobre a interação do usuário com o conteúdo do nosso site, ajudando-nos a entender melhor a eficácia do nosso conteúdo de e-mail e website.',

  privacyPolicy: 'Política de Privacidade',

  subtitle: 'Você pode modificar suas preferências de privacidade a qualquer momento.',

  acceptAll: 'Aceitar todos',
  acceptAllCookies: 'Aceitar todos os cookies',

  preferences: 'Preferências',
  savePreferences: 'Salvar preferências'
};

//CORES
var wCookieConsentStyles = {
  titleColor: "#333",
  subtitleColor: "#333",
  linkColor:"#1d5e90",
  btnCloseColor:"#333",
  groupTitleColor: "#333",
  groupBackgroundColor: "#ededed",
  modalBackgroundColor:"#fefefe",
  modalBorderColor:"#ccc",
  modalTextColor: "#222",
  modalBtnBackgroundColor: "#1abc9c",
  modalBtnBorderColor: "#16a085",
  modalBtnFontColor:"#ecf0f1",
  barBackgroundColor:"#fefefe",
  barBorderColor:"#e0dcdc",
  barTextColor:"#333",
  barBtnBackgroundColor: "#1abc9c",
  barBtnBorderColor: "#16a085",
  barBtnFontColor:"#ecf0f1",
  sliderColor: "#2196F3"
}

//DOMÍNIOS DOS COOKIES
var wCookieRootCookieDomain = null;

// DEFINE OS LISTENERS
function wCookieConsentSetListeners(){
  //MODAL
  document.getElementById('wCookieConsentBar-openPreferences').addEventListener('click',wCookieConsentOpenModal);
  document.getElementById('wCookieConsentModal-closePreferences').addEventListener('click',wCookieConsentCloseModal);

  //SAVE PREFERENCES
  document.getElementById('wCookieConsentModal-savePreferences').addEventListener('click',wCookieConsentSavePreferences);

  //ACCEPT ALL
  document.getElementById('wCookieConsentBar-acceptAll').addEventListener('click',wCookieConsentAcceptAll);
  document.getElementById('wCookieConsentModal-acceptAll').addEventListener('click',wCookieConsentAcceptAll);
}

//MÉTODO RESPONSÁVEL POR VERIFICAR COOKIES DE PERFORMANCE
function wCookieConsentVerifyPerformance(){
  return wCookieConsentGetCookie(WCOOKIE_CONSENT_PERFORMANCE) == "true";
}

//MÉTODO RESPONSÁVEL POR VERIFICAR COOKIES DE MARKETING
function wCookieConsentVerifyMarketing(){
  return wCookieConsentGetCookie(WCOOKIE_CONSENT_MARKETING) == "true";
}

//MÉTODO RESPONSÁVEL POR VERIFICAR COOKIES FUNCIONAIS
function wCookieConsentVerifyFunctional(){
  return wCookieConsentGetCookie(WCOOKIE_CONSENT_FUNCTIONAL) == "true";
}

//CARREGA AS PREFERÊNCIAS DE COOKIES
function wCookieConsentLoadPreferences(){
  //COOKIES PERFORMANCE
  let performance = wCookieConsentVerifyPerformance();
  wCookieConsentCheckPerformance.checked = performance;

  //REMOVE OS COOKIES PADRÕES DE PERFORMANCE
  if(!performance){
    wCookieConsentUnsetCookie('produto/visitado');
  }

  //COOKIES FUNCIONAIS
  wCookieConsentCheckFunctional.checked = wCookieConsentVerifyFunctional();

  //COOKIES DE MARKETING
  let marketing = wCookieConsentVerifyMarketing();
  wCookieConsentCheckMarketing.checked = marketing;

  //REMOVE OS COOKIES PADRÕES DE MARKETING
  if(!marketing){
    wCookieConsentUnsetCookie('Cliente/Email');
  }
}

//EXIBE A BARRA INICIAL
function wCookieConsentShowBar(){
  //VERIFICA O COOKIE QUE OCULTA A BARRA
  if(wCookieConsentGetCookie(WCOOKIE_CONSENT) == "hide"){
    wCookieConsentHideBar();
    return false;
  }

  //EXIBE A BARRA
  wCookieConsentBar.style.display = 'block';
}

//ESCONDE A BARRA INICIAL
function wCookieConsentHideBar(){
  //HIDE BAR
  wCookieConsentSetCookie(WCOOKIE_CONSENT,'hide');
  wCookieConsentBar.style.display = 'none';

  //CLOSE MODAL
  wCookieConsentCloseModal();

  //RECARREGA OS DADOS DE COOKIES
  wCookieConsentLoadPreferences();
}

//ESCONDE A BARRA INICIAL
function wCookieConsentSavePreferences(){
  //COOKIE DE CONSENTIMENTO PERFORMANCE
  wCookieConsentSetCookie(WCOOKIE_CONSENT_PERFORMANCE,wCookieConsentCheckPerformance.checked);

  //COOKIE DE CONSENTIMENTO MARKETING
  wCookieConsentSetCookie(WCOOKIE_CONSENT_MARKETING,wCookieConsentCheckMarketing.checked);

  //COOKIE DE CONSENTIMENTO FUNCIONAL
  wCookieConsentSetCookie(WCOOKIE_CONSENT_FUNCTIONAL,wCookieConsentCheckFunctional.checked);

  //OCULTA A BARRA
  wCookieConsentHideBar();
}

// ABRE O MODAL DE CONSENTIMENTO
function wCookieConsentOpenModal(){
 wCookieConsentModal.style.display = 'block';
}

// FECHA O MODAL DE CONSENTIMENTO
function wCookieConsentCloseModal(){
 wCookieConsentModal.style.display = 'none';
}

// ACEITA TODOS OS COOKIES
function wCookieConsentAcceptAll(){
  //HABILITA COOKIES PERFORMANCE
  wCookieConsentSetCookie(WCOOKIE_CONSENT_PERFORMANCE,"true");

  //HABILITA COOKIES DE MARKETING
  wCookieConsentSetCookie(WCOOKIE_CONSENT_MARKETING,"true");

  //HABILITA COOKIES DE MARKETING
  wCookieConsentSetCookie(WCOOKIE_CONSENT_FUNCTIONAL,"true");

  //OCULTA A BARRA
  wCookieConsentHideBar();
}

// DEFINE O COOKIE
function wCookieConsentSetCookie(name, value) {
  let days = 3285;
  const d = new Date();
  d.setTime(d.getTime() + (days*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  let domain = wCookieRootCookieDomain ? ';domain='+wCookieRootCookieDomain : '';
  document.cookie = name + "=" + value + ";" + expires + domain + ";path=/";
}

// DELETA O COOKIE
function wCookieConsentUnsetCookie(name) {
  let value = "";
  let expires = "expires=Thu, 01 Jan 1970 00:00:01 GMT";
  let domain = wCookieRootCookieDomain ? ';domain='+wCookieRootCookieDomain : '';
  document.cookie = name + "=" + value + ";" + expires + domain + ";path=/";
}

// OBTÉM UM COOKIE
function wCookieConsentGetCookie(name) {
  name = name + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

//ALTERA OS VALORES DAS VARIÁVEIS DO CSS
function wCookieConsentSetStyles(styles){
   wCookieConsentStyles.titleColor              = styles.titleColor ?? wCookieConsentStyles.titleColor;
   wCookieConsentStyles.subtitleColor           = styles.subtitleColor ?? wCookieConsentStyles.subtitleColor;
   wCookieConsentStyles.linkColor               = styles.linkColor ?? wCookieConsentStyles.linkColor;
   wCookieConsentStyles.btnCloseColor           = styles.btnCloseColor ?? wCookieConsentStyles.btnCloseColor;
   wCookieConsentStyles.groupTitleColor         = styles.groupTitleColor ?? wCookieConsentStyles.groupTitleColor;
   wCookieConsentStyles.groupBackgroundColor    = styles.groupBackgroundColor ?? wCookieConsentStyles.groupBackgroundColor;
   wCookieConsentStyles.modalBackgroundColor    = styles.modalBackgroundColor ?? wCookieConsentStyles.modalBackgroundColor;
   wCookieConsentStyles.modalBorderColor        = styles.modalBorderColor ?? wCookieConsentStyles.modalBorderColor;
   wCookieConsentStyles.modalTextColor          = styles.modalTextColor ?? wCookieConsentStyles.modalTextColor;
   wCookieConsentStyles.modalBtnBackgroundColor = styles.modalBtnBackgroundColor ?? wCookieConsentStyles.modalBtnBackgroundColor;
   wCookieConsentStyles.modalBtnBorderColor     = styles.modalBtnBorderColor ?? wCookieConsentStyles.modalBtnBorderColor;
   wCookieConsentStyles.modalBtnFontColor       = styles.modalBtnFontColor ?? wCookieConsentStyles.modalBtnFontColor;
   wCookieConsentStyles.barBackgroundColor      = styles.barBackgroundColor ?? wCookieConsentStyles.barBackgroundColor;
   wCookieConsentStyles.barBorderColor          = styles.barBorderColor ?? wCookieConsentStyles.barBorderColor;
   wCookieConsentStyles.barTextColor            = styles.barTextColor ?? wCookieConsentStyles.barTextColor;
   wCookieConsentStyles.barBtnBackgroundColor   = styles.barBtnBackgroundColor ?? wCookieConsentStyles.barBtnBackgroundColor;
   wCookieConsentStyles.barBtnBorderColor       = styles.barBtnBorderColor ?? wCookieConsentStyles.barBtnBorderColor;
   wCookieConsentStyles.barBtnFontColor         = styles.barBtnFontColor ?? wCookieConsentStyles.barBtnFontColor;
   wCookieConsentStyles.sliderColor             = styles.sliderColor ?? wCookieConsentStyles.sliderColor;
}

//ALTERA OS TEXTOS PADRÕES
function wCookieConsentSetTexts(texts){
  //TEXT BAR
  wCookieConsentTexts.textBar = texts.textBar ?? wCookieConsentTexts.textBar;


  //TÍTULO DOS COOKIES OBRIGATÓRIOS
  wCookieConsentTexts.strictTitle = texts.strictTitle ?? wCookieConsentTexts.strictTitle;

  //DESCRIÇÃO DOS COOKIES OBRIGATÓRIOS
  wCookieConsentTexts.strictDescription = texts.strictDescription ?? wCookieConsentTexts.strictDescription;


  //TÍTULO DOS COOKIES DE PERFORMANCE
  wCookieConsentTexts.performanceTitle = texts.performanceTitle ?? wCookieConsentTexts.performanceTitle;

  //DESCRIÇÃO DOS COOKIES DE PERFORMANCE
  wCookieConsentTexts.performanceDescription = texts.performanceDescription ?? wCookieConsentTexts.performanceDescription;


  //TÍTULO DOS COOKIES FUNCIONAIS
  wCookieConsentTexts.functionalTitle = texts.functionalTitle ?? wCookieConsentTexts.functionalTitle;

  //DESCRIÇÃO DOS COOKIES FUNCIONAIS
  wCookieConsentTexts.functionalDescription = texts.functionalDescription ?? wCookieConsentTexts.functionalDescription;


  //TÍTULO DOS COOKIES DE MARKETING
  wCookieConsentTexts.marketingTitle = texts.marketingTitle ?? wCookieConsentTexts.marketingTitle;

  //DESCRIÇÃO DOS COOKIES DE MARKETING
  wCookieConsentTexts.marketingDescription = texts.marketingDescription ?? wCookieConsentTexts.marketingDescription;


  //TEXTO AO FINAL DA POP-UP
  wCookieConsentTexts.subtitle = texts.subtitle ?? wCookieConsentTexts.subtitle;


  //TEXTO DO LINK PARA AS POLÍTICAS DE PRIVACIDADE
  wCookieConsentTexts.privacyPolicy = texts.privacyPolicy ?? wCookieConsentTexts.privacyPolicy;


  //ACEITAR TODOS - BOTÃO
  wCookieConsentTexts.acceptAll = texts.acceptAll ?? wCookieConsentTexts.acceptAll;

  //ACEITAR TODO OS COOKIES - BOTÃO
  wCookieConsentTexts.acceptAllCookies = texts.acceptAllCookies ?? wCookieConsentTexts.acceptAllCookies;


  //PREFERÊNCIAS - BOTÃO
  wCookieConsentTexts.preferences = texts.preferences ?? wCookieConsentTexts.preferences;

  //SALVAR PREFERÊNCIAS - BOTÃO
  wCookieConsentTexts.savePreferences = texts.savePreferences ?? wCookieConsentTexts.savePreferences;
}

//DEFINE O DOMÍNIO DO COOKIE (USADO EM PROJETOS MULTIDOMÍNIOS)
function wCookieConsentSetCookieDomain(rootDomain){
  wCookieRootCookieDomain = rootDomain;
}

//RENDERIZA O HTML DO GERENCIADOR DE COOKIES
function wCookieConsentRenderHTML(title,domain,policyUrl){
  //HTML
  let wCookieHTML = '\
  <style>\
  :root {\
    --wCookieConsent-titleColor: '+wCookieConsentStyles.titleColor+';\
    --wCookieConsent-subtitleColor: '+wCookieConsentStyles.subtitleColor+';\
    --wCookieConsent-groupTitleColor: '+wCookieConsentStyles.groupTitleColor+';\
    --wCookieConsent-groupBackgroundColor: '+wCookieConsentStyles.groupBackgroundColor+';\
    --wCookieConsent-linkColor: '+wCookieConsentStyles.linkColor+';\
    --wCookieConsent-btnCloseColor: '+wCookieConsentStyles.btnCloseColor+';\
    --wCookieConsent-modalBackgroundColor: '+wCookieConsentStyles.modalBackgroundColor+';\
    --wCookieConsent-modalBorderColor: '+wCookieConsentStyles.modalBorderColor+';\
    --wCookieConsent-modalTextColor: '+wCookieConsentStyles.modalTextColor+';\
    --wCookieConsent-modalBtnBackgroundColor: '+wCookieConsentStyles.modalBtnBackgroundColor+';\
    --wCookieConsent-modalBtnBorderColor: '+wCookieConsentStyles.modalBtnBorderColor+';\
    --wCookieConsent-modalBtnFontColor: '+wCookieConsentStyles.modalBtnFontColor+';\
    --wCookieConsent-barBackgroundColor: '+wCookieConsentStyles.barBackgroundColor+';\
    --wCookieConsent-barBorderColor: '+wCookieConsentStyles.barBorderColor+';\
    --wCookieConsent-barTextColor: '+wCookieConsentStyles.barTextColor+';\
    --wCookieConsent-barBtnBackgroundColor: '+wCookieConsentStyles.barBtnBackgroundColor+';\
    --wCookieConsent-barBtnBorderColor: '+wCookieConsentStyles.barBtnBorderColor+';\
    --wCookieConsent-barBtnFontColor: '+wCookieConsentStyles.barBtnFontColor+';\
    --wCookieConsent-sliderColor: '+wCookieConsentStyles.sliderColor+';\
  }\
  #wCookieConsentContainer{\
    display:none;\
  }\
  </style>\
  <div id="wCookieConsentModal">\
      <div class="wCookieConsentModal-container">\
        <div class="wCookieConsentModal-box">\
            <div class="wCookieConsentModal-close" id="wCookieConsentModal-closePreferences">X</div>\
            <div class="wCookieConsentModal-title">'+title+'</div>\
            <div class="wCookieConsentModal-policy"><a href="'+policyUrl+'" target="_blank">'+wCookieConsentTexts.privacyPolicy+'</a></div>\
  \
            <div class="wCookieConsentModal-groups">\
              <div class="wCookieConsentModal-group">\
                <div class="wCookieConsentModal-groupTitle">'+wCookieConsentTexts.strictTitle+'</div>\
                <div class="wCookieConsentModal-groupText">'+wCookieConsentTexts.strictDescription+'</div>\
              </div>\
  \
              <div class="wCookieConsentModal-group">\
                <div class="wCookieConsentModal-groupHeader">\
                  <div class="wCookieConsentModal-groupTitle">'+wCookieConsentTexts.performanceTitle+'</div>\
                  <div class="wCookieConsentModal-groupCheckbox">\
  \
                    <label class="wCookieConsentModal-switch">\
                      <input type="checkbox" id="wCookieConsentCookie-performance">\
                      <span class="wCookieConsentModal-slider"></span>\
                    </label>\
  \
                  </div>\
                </div>\
                <div class="wCookieConsentModal-groupText">'+wCookieConsentTexts.performanceDescription+'</div>\
              </div>\
  \
              <div class="wCookieConsentModal-group">\
                <div class="wCookieConsentModal-groupHeader">\
                  <div class="wCookieConsentModal-groupTitle">'+wCookieConsentTexts.functionalTitle+'</div>\
                  <div class="wCookieConsentModal-groupCheckbox">\
  \
                    <label class="wCookieConsentModal-switch">\
                      <input type="checkbox" id="wCookieConsentCookie-funcional">\
                      <span class="wCookieConsentModal-slider"></span>\
                    </label>\
  \
                  </div>\
                </div>\
                <div class="wCookieConsentModal-groupText">'+wCookieConsentTexts.functionalDescription+'</div>\
              </div>\
  \
              <div class="wCookieConsentModal-group">\
                <div class="wCookieConsentModal-groupHeader">\
                  <div class="wCookieConsentModal-groupTitle">'+wCookieConsentTexts.marketingTitle+'</div>\
                  <div class="wCookieConsentModal-groupCheckbox">\
  \
                    <label class="wCookieConsentModal-switch">\
                      <input type="checkbox" id="wCookieConsentCookie-marketing">\
                      <span class="wCookieConsentModal-slider"></span>\
                    </label>\
  \
                  </div>\
                </div>\
                <div class="wCookieConsentModal-groupText">'+wCookieConsentTexts.marketingDescription+'</div>\
              </div>\
            </div>\
  \
            <div class="wCookieConsentModal-subtitle">'+wCookieConsentTexts.subtitle+'</div>\
  \
            <div class="wCookieConsentModal-footer">\
              <button class="wCookieConsentModal-buttonPreferences" id="wCookieConsentModal-savePreferences">'+wCookieConsentTexts.savePreferences+'</button>\
              <button class="wCookieConsent-button" id="wCookieConsentModal-acceptAll">'+wCookieConsentTexts.acceptAllCookies+'</button>\
            </div>\
        </div>\
      </div>\
    </div>\
  \
    <div class="wCookieConsentBar-container" id="wCookieConsentBar">\
      <div class="wCookieConsentBar-box">\
        <div class="wCookieConsentBar-text">'+wCookieConsentTexts.textBar+'</div>\
        <div class="wCookieConsentBar-buttons">\
          <button class="wCookieConsentBar-buttonPreferences" id="wCookieConsentBar-openPreferences">'+wCookieConsentTexts.preferences+'</button>\
          <button class="wCookieConsent-button" id="wCookieConsentBar-acceptAll">'+wCookieConsentTexts.acceptAll+'</button>\
        </div>\
      </div>\
    </div>';

    //DIV COMPLETA
    let wCookieConsentDiv = document.createElement('div');

    //DEFINE O ID
    wCookieConsentDiv.setAttribute("id", "wCookieConsentContainer");

    //ADICIONA O HTML NA DIV
    wCookieConsentDiv.innerHTML += wCookieHTML;

    //ADICIONA O HTML NA PÁGINA
    document.body.appendChild(wCookieConsentDiv);
}


//INICIA O WAP COOKIE CONSENT
function wCookieConsentInit(title,domain,policyUrl){
    //RENDERIZA O HTML
    wCookieConsentRenderHTML(title,domain,policyUrl);

    //BARRA PADRÃO
    wCookieConsentBar = document.getElementById('wCookieConsentBar');

    //MODAL
    wCookieConsentModal = document.getElementById('wCookieConsentModal');

    //CHECKBOX
    wCookieConsentCheckPerformance  = document.getElementById('wCookieConsentCookie-performance');
    wCookieConsentCheckFunctional  = document.getElementById('wCookieConsentCookie-funcional');
    wCookieConsentCheckMarketing = document.getElementById('wCookieConsentCookie-marketing');

    //LOAD PREFERENCES
    wCookieConsentLoadPreferences();

    //LISTENERS
    wCookieConsentSetListeners();

    //EXIBE A BARRA
    wCookieConsentShowBar();
}